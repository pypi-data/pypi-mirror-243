# Copyright 2004-2023 Bright Computing Holding BV
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import annotations

import hashlib
import logging
from datetime import datetime
from enum import Enum, auto
from functools import lru_cache
from typing import Any

import tenacity

from clusterondemand import utils
from clusterondemand.exceptions import CODException
from clusterondemandaws.ec2connection import create_ec2_resource_client
from clusterondemandconfig import config

from . import efs

log = logging.getLogger("cluster-on-demand")
BCM_TYPE_HEAD_NODE = "Head node"
BCM_TAG_NO_PUBLIC_IP = "BCM No public IP"


def construct_bright_tags(cluster_name, obj_name, bcm_type=None):
    tags = {
        "BCM Created at": datetime.utcnow().isoformat() + "Z",  # fix missing timezone
        "BCM Created by": utils.get_user_at_fqdn_hostname(),
        "BCM Cluster": cluster_name,
        "BCM Bursting": "on-demand",
        # This one has to follow a slightly different naming convention (i.e. no "BCM"
        # prefix), because this tag has a special meaning for AWS.
        "Name": obj_name
    }
    if bcm_type:
        tags["BCM Type"] = bcm_type
        if bcm_type == BCM_TYPE_HEAD_NODE and not config.get("head_node_assign_public_ip", True):
            tags[BCM_TAG_NO_PUBLIC_IP] = ""

    tags.update({str(k): str(v) for k, v in config.get("cluster_tags", [])})
    tags = [{"Key": key, "Value": value} for key, value in tags.items()]
    return tags


class Cluster:
    # AWS eIP assignment failures occur rarely and can be worked around
    # by retrying for 2.5+ minutes (see CM-9991).
    # Let's make it 5 minutes to make sure we don't leave an eIP allocation unassigned,
    # which costs money.
    IP_ASSIGNMENT_RETRY_DELAY = 10
    IP_ASSIGNMENT_RETRIES = 30

    def __init__(self, aws_session, name, head_node_image=None, vpc=None):
        self.efs_client = aws_session.client("efs")
        self.ec2, self.ec2c = create_ec2_resource_client(aws_session)
        self.name = name
        self.head_node_image = head_node_image
        self.vpc = vpc
        self.primary_head_node = None
        self.secondary_head_node = None
        self.active_head_node = None
        self.passive_head_node = None
        self.set_primary_secondary_head_nodes()
        self.is_ha = bool(self.secondary_head_node)
        self.set_active_passive_head_nodes()
        self.error_message = None

    @classmethod
    def get_vpc_name(cls, vpc):
        for tag in vpc.tags:
            if tag["Key"] == "Name":
                return tag["Value"]

        raise CODException("No Name tag found")

    @classmethod
    def find(cls, aws_session, names):
        ec2, _ = create_ec2_resource_client(aws_session)
        patterns = [f"{config['fixed_cluster_prefix']}{name}" for name in names]
        log.debug("Searching for vpcs with tag:name %s" % patterns)
        for vpc in ec2.vpcs.filter(
                Filters=[{"Name": "tag:Name",
                          "Values": patterns}]):
            vpc_name = cls.get_vpc_name(vpc)
            cluster_name = vpc_name[len(config["fixed_cluster_prefix"]):]
            yield cls(aws_session, cluster_name, vpc=vpc)

    def __unicode__(self):
        return "{} {!r} {!r} {}".format(self.name,
                                        self.vpc,
                                        self.primary_head_node,
                                        self.primary_head_node and self.primary_head_node.state["Name"])

    def find_head_nodes(self):
        if not self.vpc:
            return None

        instances = list(self.vpc.instances.filter(Filters=[
            {"Name": "tag:BCM Type", "Values": [BCM_TYPE_HEAD_NODE]},
            {"Name": "instance-state-name",
             "Values": ["pending", "running", "shutting-down", "stopping", "stopped"]},
        ]))
        if not instances:
            return None

        return instances

    def set_primary_secondary_head_nodes(self):
        head_nodes = self.find_head_nodes()
        if not head_nodes:
            return

        if len(head_nodes) == 1:
            self.primary_head_node, self.secondary_head_node = head_nodes[0], None
        elif len(head_nodes) == 2:
            first_hn_ha_tag = next((tag["Value"] for tag in head_nodes[0].tags if tag.get("Key") == "BCM HA"), None)
            # Without a proper tag we can't be sure which headnode is primary
            if not first_hn_ha_tag:
                raise CODException(f"Expected tag 'BCM HA' not found for cluster {self.name}, cannot determine "
                                   f"primary and secondary head nodes")

            if first_hn_ha_tag not in ["Primary", "Secondary"]:
                raise CODException(f"Expected values for 'BCM HA' tag not found for cluster {self.name}, "
                                   f"cannot determine primary and secondary head nodes")

            if first_hn_ha_tag == "Secondary":
                head_nodes.reverse()
            self.primary_head_node, self.secondary_head_node = head_nodes
        else:
            raise CODException(f"More than two head nodes found for cluster {self.name} (vpc: {self.vpc})")

    def set_active_passive_head_nodes(self):
        if not self.is_ha:
            return

        if len(self.map_head_node_type_to_address(self.primary_head_node)) == 2:
            self.active_head_node = self.primary_head_node
            self.passive_head_node = self.secondary_head_node
        elif len(self.map_head_node_type_to_address(self.secondary_head_node)) == 2:
            self.active_head_node = self.secondary_head_node
            self.passive_head_node = self.primary_head_node
        else:
            raise CODException(f"Unable to determine active headnode for cluster {self.name}, neither of the head "
                               f"nodes has HA ip address assigned.")

    @lru_cache
    def map_head_node_type_to_address(self, instance) -> dict[Cluster.IpType, Any]:
        """
        This function extracts private_ip_addresses from an instance object and determines which private_ip_address is
        A, B or HA. private_ip_addresses is a list of: [private_ip_address, private_ip_address]

        :param: instance: boto3.resources.factory.ec2.Instance
        :return: {self.IpType.A: {private_ip_address}, ...}
        """
        head_node_type_to_address_map = {}
        instance.reload()
        network_interface = instance.network_interfaces[0]  # We only use the first interface
        network_interface.reload()
        private_ip_addresses = network_interface.private_ip_addresses
        log.debug(f"Instance {instance.id} has following IP addresses attached: {private_ip_addresses}")
        for private_ip_address in private_ip_addresses:
            if not private_ip_address["Primary"]:
                # HA address is always 'Primary': False
                head_node_type_to_address_map[self.IpType.HA] = private_ip_address
            elif instance.id == self.primary_head_node.id:
                head_node_type_to_address_map[self.IpType.A] = private_ip_address
            else:
                head_node_type_to_address_map[self.IpType.B] = private_ip_address
        return head_node_type_to_address_map

    class IpType(Enum):
        A = auto()
        B = auto()
        HA = auto()

    def tag_eip(self, ip_type, epialloc_id):
        if not epialloc_id:
            return

        tags = {
            "Name": {
                self.IpType.A: f"{self.name}-a public IP",
                self.IpType.B: f"{self.name}-b public IP",
                self.IpType.HA: f"{self.name} HA public IP",
            }[ip_type],
        }
        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.NetworkInterface.create_tags
        self.ec2.create_tags(
            Resources=[epialloc_id],
            Tags=[{"Key": k, "Value": v} for k, v in tags.items()],
        )

    def allocate_address_in_vpc(self, name=None):
        allocate_address_name = f"{self.name}-{name} public IP"
        return self.ec2c.allocate_address(Domain="vpc",
                                          TagSpecifications=[{
                                              "ResourceType": "elastic-ip",
                                              "Tags": construct_bright_tags(self.name, allocate_address_name)
                                          }]
                                          )

    def create_nat_gateway(self, subnet, allocation_id=None):
        kwargs = {"SubnetId": subnet.id}
        nat_gateway_name = f"{self.name} NAT Gateway"
        kwargs["TagSpecifications"] = [{"ResourceType": "natgateway",
                                        "Tags": construct_bright_tags(self.name, nat_gateway_name)}]
        if allocation_id:
            kwargs["AllocationId"] = allocation_id

        response = self.ec2c.create_nat_gateway(**kwargs)

        if 'NatGateway' not in response:
            raise CODException("Broken response, 'NatGateway' not included when creating NAT gateway")
        if 'FailureCode' in response['NatGateway']:
            raise CODException(f"NAT gateway creation failed, {response['NatGateway']['FailureCode']}: "
                               f"{response['NatGateway']['FailureMessage']}")

        log.debug(f"Creating NAT gateway {subnet.name} NAT gateway with property: {response['NatGateway']}")
        return response['NatGateway']

    def wait_nat_gateway_state(self, nat_gateway_id, state):
        log.info(f"Waiting NAT gateway {nat_gateway_id} to become {state}...")
        if state == 'available':
            waiter = self.ec2c.get_waiter('nat_gateway_available')
        elif state == 'deleted':
            waiter = self.ec2c.get_waiter('nat_gateway_deleted')
        else:
            assert ("Not supported NAT gateway status poll")

        waiter.wait(
            Filters=[{
                'Name': 'state',
                'Values': [state]
            }],
            NatGatewayIds=[nat_gateway_id]
        )

    def allocate_and_associate_head_node_eips(self, instance) -> list[tuple[Any, Any, Any]]:
        """
        Sometimes the instance does not have a public EIP attached to a private ip address (E.g. creating or starting),
        This function will allocate an EIP, then associate it for every private ip address of the instance.
        If the interface already has public IP, it will be returned, instead of (re)attaching a new one.

        :param: instance: boto3.resources.factory.ec2.Instance
        :return: private_ip_addresses: [(ip_type, allocation_id, allocation_ip)]
        """
        @tenacity.retry(
            wait=tenacity.wait_exponential(multiplier=1, max=self.IP_ASSIGNMENT_RETRY_DELAY),
            stop=tenacity.stop_after_attempt(self.IP_ASSIGNMENT_RETRIES),
            before_sleep=tenacity.before_sleep_log(log, logging.DEBUG),
            after=tenacity.after_log(log, logging.DEBUG),
            reraise=True,
        )
        def associate_address(allocation_id, instance_id, private_ip):
            # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.associate_address
            self.ec2c.associate_address(
                AllocationId=allocation_id,
                InstanceId=instance_id,
                PrivateIpAddress=private_ip,
            )

        ip_types_and_allocations = []
        private_ip_addresses = self.map_head_node_type_to_address(instance)

        for ip_type, private_ip_address in private_ip_addresses.items():
            if private_ip_address.get("Association"):  # A public EIP is bound to the private_ip_address
                allocation_id = private_ip_address.get("Association")["AllocationId"]
                allocation_ip = private_ip_address.get("Association")["PublicIp"]
                ip_types_and_allocations.append((ip_type, allocation_id, allocation_ip))
                log.debug(f"Public IP {allocation_ip} is already used as address '{ip_type.name}', "
                          f"skipping allocation and association")
                continue

            allocation = self.allocate_address_in_vpc(name="headnode")
            allocation_id = allocation["AllocationId"]
            allocation_ip = allocation["PublicIp"]
            private_ip = private_ip_address["PrivateIpAddress"]
            log.debug(f"Allocated public IP {allocation_ip} with allocation_id: {allocation_id}.")

            try:
                associate_address(allocation_id, instance.id, private_ip)
                self.tag_eip(ip_type, allocation_id)
                ip_types_and_allocations.append((ip_type, allocation_id, allocation_ip))
                instance.reload()  # Need to reload after EIP assignment, or instance.public_ip_address will be empty
                log.debug(f"Associated public IP {allocation_ip} with instance {instance.id} as address "
                          f"'{ip_type.name}'.")
            except Exception as associate_error:
                self.ec2c.release_address(AllocationId=allocation_id)
                log.error(f"Error associating IP {allocation_ip} as {ip_type.name} address to {instance.id}.")
                raise CODException("Error associating IP", caused_by=associate_error)

        return ip_types_and_allocations

    def attach_eips_to_head_nodes(self):
        if any(tag["Key"] == BCM_TAG_NO_PUBLIC_IP for tag in self.primary_head_node.tags):
            log.info(f"Head node has {BCM_TAG_NO_PUBLIC_IP!r} tag, so no public IPs will not be allocated")
            return

        if not self.is_ha:
            ip_types_and_allocations = self.allocate_and_associate_head_node_eips(self.primary_head_node)
            log.info(f"Cluster {self.name} IP: {ip_types_and_allocations[0][2]}")
        else:
            ip_types_and_allocations = self.allocate_and_associate_head_node_eips(self.primary_head_node) + \
                self.allocate_and_associate_head_node_eips(self.secondary_head_node)

            log.info(f"Cluster {self.name} IPs: "
                     f"{', '.join([i[2] + ' ' + f'({i[0].name})' for i in ip_types_and_allocations])}")

    def disassociate_and_release_head_node_eips(self, instance):
        """
        If public EIP is attached to the private IP address of the instance, disassociate and then release it. Used when
        stopping or terminating the instance
        :param: instance: boto3.resources.factory.ec2.Instance
        :return:
        """
        instance_private_addresses = self.map_head_node_type_to_address(instance)
        for private_ip_address in instance_private_addresses.values():
            if not private_ip_address.get("Association"):  # A public EIP is not bound to the private_ip_address
                log.debug(f"Private IP address {private_ip_address['PrivateIpAddress']} on {instance.id} has "
                          f"no Elastic IP associated, nothing to release")
                continue

            eip_assoc = private_ip_address.get("Association")

            # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.disassociate_address
            log.debug(f"Disassociating AssociationId: {eip_assoc.get('AssociationId')} "
                      f"(EIP: {eip_assoc.get('PublicIp')})")
            self.ec2c.disassociate_address(AssociationId=eip_assoc.get("AssociationId"))

            # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.release_address
            log.debug(f"Releasing IP allocation {eip_assoc.get('AllocationId')} "
                      f"for public IP: {eip_assoc.get('PublicIp')})")
            self.ec2c.release_address(AllocationId=eip_assoc.get("AllocationId"))

            log.debug(f"Elastic IP {eip_assoc.get('PublicIp')} was detached from instance {instance.id}")

    def detach_eips_from_head_nodes(self):
        if self.primary_head_node is not None:
            self.disassociate_and_release_head_node_eips(self.primary_head_node)
        if self.is_ha and self.secondary_head_node is not None:
            self.disassociate_and_release_head_node_eips(self.secondary_head_node)

    def get_efs_id(self):
        # The creation token is originally generated by cm-cloud-ha (see cluster-tools repo)
        # To be backward compatible, we check using both the old format and the new format
        old_efs_creation_token = f"bcm-ha-efs-{self.name}"
        efs_creation_token = hashlib.sha256(f"bcm-ha-efs-{self.name}".encode()).hexdigest()

        response = efs.describe_fs(self.efs_client, token=efs_creation_token)
        if response:
            return response["FileSystemId"]

        if len(old_efs_creation_token) <= 64:
            response = efs.describe_fs(self.efs_client, token=old_efs_creation_token)
            return response["FileSystemId"] if response else None

        return None

    def try_delete_efs(self):
        fs_id = self.get_efs_id()
        if not fs_id:
            return

        log.info(f"Deleting EFS {fs_id}...")
        response = efs.describe_mount_target(self.efs_client, fs_id=fs_id)
        if response:
            efs.delete_mount_target(self.efs_client, response["MountTargetId"])
        efs.delete_fs(self.efs_client, fs_id)

    def terminate_instances_for_vpc(self):
        vpc_name = self.get_vpc_name(self.vpc)
        log.info(f"Finding instances for VPC '{vpc_name}'...")
        instances = [instance for instance in self.vpc.instances.all()]

        if not instances:
            log.info(f"No instances found in VPC '{vpc_name}'")
            return

        # We want to terminate all instances here and wait until they are terminated.
        # That should be faster than
        # request termination and wait sequentially in destroy_vpc methods
        log.info(f"Issuing termination requests for {len(instances)} instances for VPC '{vpc_name}'...")
        for instance in instances:
            instance.terminate()

        log.info(f"Waiting until instances of VPC '{vpc_name}' are terminated...")
        for instance in instances:
            instance.wait_until_terminated()

    def destroy_vpc(self):
        vpc_name = self.get_vpc_name(self.vpc)
        log.info(f"Destroying VPC '{vpc_name}'")

        log.info(f"Deleting subnets of VPC '{vpc_name}'...")
        for subnet in self.vpc.subnets.all():
            subnet.delete()

        log.info(f"Deleting route tables of VPC '{vpc_name}'...")
        for route_table in self.vpc.route_tables.all():
            if not self._is_main_routing_table(route_table):
                route_table.delete()

        log.info(f"Detaching and deleting gateways of VPC '{vpc_name}'...")
        for gateway in self.vpc.internet_gateways.all():
            self.vpc.detach_internet_gateway(InternetGatewayId=gateway.id)
            gateway.delete()

        # Flush all permissions, because if they refer to security group,
        # that security group won't be deleted
        log.info(f"Flushing permissions of security groups of VPC '{vpc_name}'...")
        for sg in self.vpc.security_groups.all():
            if sg.ip_permissions:
                sg.revoke_ingress(IpPermissions=sg.ip_permissions)
            if sg.ip_permissions_egress:
                sg.revoke_egress(IpPermissions=sg.ip_permissions_egress)

        # Delete security groups themselves
        log.info(f"Deleting security groups of VPC '{vpc_name}'...")
        for sg in self.vpc.security_groups.all():
            if sg.group_name != "default":
                sg.delete()

        log.info(f"Deleting VPC '{vpc_name}'...")
        self.vpc.delete()

        log.info(f"Done destroying VPC '{vpc_name}'")

    def destroy_nat_gateways(self):
        response = self.ec2c.describe_nat_gateways(
            Filter=[
                {
                    'Name': 'vpc-id',
                    'Values': [self.vpc.id]
                }
            ]
        )
        nat_gateways = response['NatGateways']
        for nat_gateway in nat_gateways:
            if nat_gateway['State'] in ['deleting', 'deleted']:
                continue
            nat_gateway_id = nat_gateway['NatGatewayId']
            self.ec2c.delete_nat_gateway(NatGatewayId=nat_gateway_id)
            self.wait_nat_gateway_state(nat_gateway_id, 'deleted')
            # Extract the Elastic IP allocation ID from the response and release
            for nat_gateway_addr in nat_gateway['NatGatewayAddresses']:
                allocation_id = nat_gateway_addr['AllocationId']
                self.ec2c.release_address(AllocationId=allocation_id)

    def destroy(self):
        self.detach_eips_from_head_nodes()
        self.terminate_instances_for_vpc()
        self.destroy_nat_gateways()
        self.try_delete_efs()
        self.destroy_vpc()

        self.vpc = None
        self.primary_head_node = None

    def stop(self, release_eip):
        """
        We will try to stop the instance only if it's in "running" or "pending" state.
        Instance states: https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_InstanceState.html
        """
        running_instances = [instance for instance in self.vpc.instances.all()
                             if instance.state["Name"] in ["pending", "running"]]

        if not running_instances:
            log.info(f"No running instances found for cluster {self.name}")
            return

        if release_eip:
            self.detach_eips_from_head_nodes()

        log.info(f"Issuing stop requests for cluster {self.name}...")
        for instance in running_instances:
            log.debug(f"Stopping instance {instance.id}")
            instance.stop()

        log.info(f"Waiting for instances of {self.name} until stopped...")
        for instance in running_instances:
            instance.wait_until_stopped()

    def start(self):
        """
        We will try to start the instance only if it's not in "running" or "pending" state.
        Instance states: https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_InstanceState.html
        """
        def start_head_node(instance, head_node_type, cluster_name):
            if instance.state["Name"] in ["pending", "running"]:
                log.info(f"{head_node_type} of cluster {cluster_name} is already running, not attempting to start")
                return

            log.info(f"Starting {head_node_type} node of {cluster_name}...")
            instance.start()
            log.info(f"Waiting until {head_node_type} of {cluster_name} is running...")
            instance.wait_until_running()

        start_head_node(self.primary_head_node, "primary head node", self.name)
        if self.is_ha:
            start_head_node(self.secondary_head_node, "secondary head node", self.name)

        self.attach_eips_to_head_nodes()

    @classmethod
    def _is_main_routing_table(cls, route_table):
        for association in route_table.associations_attribute:
            if association.get("Main"):
                return True
        return False
