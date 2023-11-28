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
import shlex
import typing

import yaml

import clusterondemand.brightsetup
from clusterondemand.cloudconfig import CloudConfig, SignalHandler
from clusterondemand.cloudconfig.headcommands import (
    add_head_node_commands,
    add_run_bright_setup_commands,
    add_wait_for_cmd_ready_commands
)
from clusterondemand.cloudconfig.headfiles import REMOTE_NODE_DISK_SETUP_PATH, add_common_head_files
from clusterondemand.configuration import CFG_NO_ADMIN_EMAIL, NO_WLM
from clusterondemandconfig import config

log = logging.getLogger("cluster-on-demand")

ERROR_HANDLER = """\
set -e
function error_handler {
    read line file <<<$(caller)
    echo \"An error occurred in line $line of $file: exit code '$1' while running: '$2'\"
    exit 1
}
trap 'error_handler $? "$BASH_COMMAND"' ERR
"""


class OCISignalHandler(SignalHandler):
    def get_init_commands(self):
        return [
            ERROR_HANDLER,
        ]

    def get_files(self):
        return []

    def get_config_complete_commands(self):
        return self.get_status_log_commands("cloud-init: Complete.")

    def get_status_log_commands(self, status: str):
        escaped_status = shlex.quote(f"{self.log_prefix} {status}")
        return [f"echo {escaped_status}"]


def generate_bright_setup(
        cluster_name: str,
        node_image_id: str,
        vcn_cidr: str,
        subnet_id: str,
        subnet_cidr: str,
        private_subnet_id: str,
        private_subnet_cidr: str,
        node_nsg_id: str,
        node_instance_configuration_id: str,
        auth_key_content: str
) -> dict[str, typing.Any]:
    license_dict = clusterondemand.brightsetup.get_license_dict(cluster_name)

    admin_email = config["admin_email"] if config["admin_email"] != CFG_NO_ADMIN_EMAIL else None

    brightsetup = clusterondemand.brightsetup.generate_bright_setup(
        cloud_type="oci",
        wlm=config["wlm"] if config["wlm"] != NO_WLM else "",
        hostname=cluster_name,
        password=config["cluster_password"],
        node_count=0,
        timezone=config["timezone"],
        admin_email=admin_email,
        license_dict=license_dict,
        node_kernel_modules=["virtio_net", "virtio_pci", "virtio_blk", "virtio_scsi", "8021q"],
        node_disk_setup_path=REMOTE_NODE_DISK_SETUP_PATH,
    )

    private_subnet = {
        "name": "oci-network-private",
        "cidr": private_subnet_cidr,
        "cloud_subnet_id": private_subnet_id,
    } if private_subnet_id else None

    brightsetup["modules"]["brightsetup"]["oci"] = {
        "api": {
            "auth_user": config["oci_user"],
            "auth_key_content": auth_key_content if not config["use_principal_authentication"] else "",
            "auth_fingerprint": config["oci_fingerprint"],
            "auth_tenancy": config["oci_tenancy"],
            "region": config["oci_region"],
        },
        "network": {
            "cidr": vcn_cidr,
            "subnets": [
                {
                    "name": "oci-network",
                    "cidr": subnet_cidr,
                    "cloud_subnet_id": subnet_id,
                },
                *([private_subnet] if private_subnet else []),
            ],
        },
        "nodes": {
            "base_name": "cnode",
            "count": config["nodes"],
            "region": config["oci_region"],
            "availability_domain": config["oci_availability_domain"] or "",
            "shape": config["node_shape"],
            "image_id": node_image_id or "",
            "compartment_id": config["compute_compartment_id"] or config["oci_compartment_id"],

            # For OCPUs/Memory 0 means "don't use the value in shape config". So, shape defaults will be used.
            "ocpus": config["node_number_cpus"] or 0,
            "memory_in_gb": config["node_memory_size"] or 0,

            "storage": {
                "root-disk": config["node_root_volume_size"],
            },
            "use_cluster_network": config["node_use_cluster_network"],
            "node_nsg_id": node_nsg_id,
            "node_instance_configuration_id": node_instance_configuration_id,
            "images_compartment_id": config["image_compartment_id"] or "",
            "images_manifest_base_url": config["community_applications_url"] or "",
        },
    }

    return brightsetup


def build_cloud_config(cm_bright_setup_conf, version, distro):
    cloud_config = CloudConfig(OCISignalHandler("Head node"))
    add_common_head_files(cloud_config, version, distro)
    cloud_config.add_file("/root/cm/cm-bright-setup.conf", yaml.dump(cm_bright_setup_conf))
    add_head_node_commands(cloud_config)
    if config["run_cm_bright_setup"]:
        add_run_bright_setup_commands(cloud_config)
        add_wait_for_cmd_ready_commands(cloud_config)
    cloud_config.add_config_complete_commands()

    return cloud_config
