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

import logging

from clusterondemand.clusternameprefix import clusterprefix_ns, ensure_cod_prefix
from clusterondemand.utils import confirm, confirm_ns, log_no_clusters_found, multithread_run
from clusterondemandaws.base import ClusterCommandBase
from clusterondemandconfig import ConfigNamespace, config

from .cluster import Cluster
from .configuration import awscommon_ns
from .ec2connection import establish_connection_to_aws

log = logging.getLogger("cluster-on-demand")


def run_command():
    return ClusterDelete().run()


config_ns = ConfigNamespace("aws.cluster.delete", "cluster delete parameters")
config_ns.import_namespace(awscommon_ns)
config_ns.import_namespace(clusterprefix_ns)
config_ns.import_namespace(confirm_ns)
config_ns.add_repeating_positional_parameter(
    "filters",
    require_value=True,
    help="Cluster names or patterns. Wildcards are supported (e.g: \\*)",
)


class ClusterDelete(ClusterCommandBase):

    def _validate_params(self):
        self._validate_aws_access_credentials()

    def run(self):
        self._validate_params()

        aws_session = establish_connection_to_aws()
        names = [ensure_cod_prefix(name) for name in config["filters"]]
        clusters = list(Cluster.find(aws_session, names))

        if not clusters:
            log_no_clusters_found("delete")
            return

        if any(c.get_efs_id() for c in clusters):
            log.warning("Some clusters have a Cloud HA EFS storage. It will also be deleted")

        if not confirm("This will destroy VPCs for %s, continue?" % (" ".join([c.name for c in clusters]),)):
            return

        multithread_run(lambda cluster: cluster.destroy(), clusters, config["max_threads"])
