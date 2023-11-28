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

import base64
import logging
import pathlib
import re
import socket
import time

import netaddr
import oci.core
import oci.pagination
import oci.util
import yaml
from oci.core.models import Instance
from oci.exceptions import ServiceError

import clusterondemand.clustercreate
from clusterondemand import utils
from clusterondemand.cidr import cidr, must_be_within_cidr, nullable_cidr
from clusterondemand.clusternameprefix import must_start_with_cod_prefix
from clusterondemand.exceptions import CODException, UserReportableException, ValidationException
from clusterondemand.inbound_traffic_rule import InboundTrafficRule
from clusterondemand.ip import ip, nth_ip_in_default_network
from clusterondemand.node_definition import NodeDefinition
from clusterondemand.ssh import clusterssh_ns
from clusterondemand.ssh_key import validate_ssh_pub_key
from clusterondemand.summary import SummaryType
from clusterondemand.wait_helpers import clusterwaiters_ns, wait_for_cluster_to_be_ready
from clusterondemandconfig import (
    ConfigNamespace,
    config,
    may_not_equal_none,
    must_be_multiple_of,
    number_must_be_between
)
from clusterondemandconfig.configuration_validation import requires_other_parameters_to_be_set
from clusterondemandoci.base import ClusterCommand
from clusterondemandoci.brightsetup import build_cloud_config, generate_bright_setup
from clusterondemandoci.cluster import Cluster
from clusterondemandoci.clusterdelete import ClusterDelete
from clusterondemandoci.const import CLUSTER_NAME_TAG, IMAGE_CREATED_TIME_TAG, IMAGE_NAME_TAG
from clusterondemandoci.summary import OCISummaryGenerator
from clusterondemandoci.utils import get_head_node_list, get_oci_key_content

from .configuration import ociclustercommon_ns, ocicommon_ns
from .images import CommunityAppImage, OCIImageSource, findimages_ns, make_cod_image_from_ocid

log = logging.getLogger("cluster-on-demand")

config_ns = ConfigNamespace("oci.cluster.create", "cluster creation parameters")
config_ns.import_namespace(ocicommon_ns)
config_ns.import_namespace(ociclustercommon_ns)
config_ns.import_namespace(findimages_ns)
config_ns.override_imported_parameter("distro", default="ubuntu2004")
config_ns.override_imported_parameter("version", default="10.0")
config_ns.override_imported_parameter("image_visibility", default="any")
config_ns.import_namespace(clusterssh_ns)
config_ns.import_namespace(clusterwaiters_ns)
config_ns.import_namespace(clusterondemand.configuration.clustercreate_ns)
config_ns.import_namespace(clusterondemand.configuration.clustercreatename_ns)
config_ns.import_namespace(clusterondemand.configuration.cmd_debug_ns)

# Adding necessary parameters for CloudConfig
config_ns.import_namespace(clusterondemand.configuration.node_disk_setup_ns)
config_ns.import_namespace(clusterondemand.configuration.append_to_bashrc_ns)
config_ns.import_namespace(clusterondemand.configuration.resolve_hostnames_ns)
config_ns.import_namespace(clusterondemand.copyfile.copyfile_ns)

config_ns.remove_imported_parameter("name")
config_ns.remove_imported_parameter("head_node_type")
config_ns.remove_imported_parameter("node_type")
config_ns.add_parameter(
    "name",
    help="Name of the cluster to create",
    validation=[may_not_equal_none, must_start_with_cod_prefix]
)
config_ns.add_parameter(
    "timezone",
    default="Europe/Amsterdam",
    help="Timezone of the cluster"
)
config_ns.add_parameter(
    "vcn_cidr",
    default=cidr("10.142.0.0/16"),
    help=(
        "CIDR range of the VCN; only used when COD is creating a VCN. Subnets created in "
        "this VCN must fall within this range. The widest allowed range is /16."
    ),
    parser=cidr
)
config_ns.add_parameter(
    "subnet_cidr",
    default=cidr("10.142.0.0/17"),
    help=(
        "CIDR range of the subnet; only used when COD is creating a subnet. The specified CIDR must "
        "fall within the range specified by '--vcn-cidr'."
    ),
    parser=cidr,
    validation=must_be_within_cidr("vcn_cidr")
)
config_ns.add_parameter(
    "private_subnet_cidr",
    default=cidr("10.142.128.0/17"),
    help=(
        "CIDR range of the subnet; only used when COD is creating a subnet. The specified CIDR must "
        "fall within the range specified by '--vcn-cidr'."
    ),
    parser=cidr,
    validation=must_be_within_cidr("vcn_cidr")
)
config_ns.add_parameter(
    "head_node_ip",
    advanced=True,
    default=lambda param, config: (
        nth_ip_in_default_network(-2, "subnet_cidr")(param, config)
        if not config["existing_subnet_id"]
        else None
    ),
    parser=lambda value: ip(value) if value else None,
    help="The private IP address of the head node",
    help_varname="IP",
)

config_ns.add_parameter(
    "ingress_icmp",
    default=None,
    help="CIDR from which to allow ingress ICMP traffic to the head node."
         "Specify 'None' to disable ICMP all together.",
    parser=nullable_cidr
)

config_ns.add_parameter(
    "head_node_nsg_id",
    advanced=True,
    help_varname="HEAD_NODE_SEC_GROUP_ID",
    help="By default the security group for the head node is created by cm-cod-oci tool. "
         "This optional parameter can be used to change this behavior by providing a pre-created security group ID. "
         "When specifying it, make sure to allow bidirectional access between the head node's SG and node's SG. Also "
         "the sec group should allow for inbound TCP 8081 from the host running the tool, "
         "otherwise '--cloud-init-timeout 0' should be set."
         "If you want to tweak the sec. groups created by the cm-cod-oci tool, use --ingress-rules. "
         "Related parameters: --node-sg-id",
    validation=requires_other_parameters_to_be_set(["node_nsg_id"])
)

config_ns.add_parameter(
    "node_nsg_id",
    advanced=True,
    help_varname="NODE_SEC_GROUP_ID",
    help="By default the security group for the compute nodes is created by cm-cod-oci tool. "
         "This optional parameter can be used to change this behavior by providing a pre-created security group ID. "
         "Make sure to allow bidirectional access between the head node's SG and node's SG. "
         "Related parameter: --head-node-sg-id",
    validation=requires_other_parameters_to_be_set(["head_node_nsg_id"])
)

config_ns.add_enumeration_parameter(
    "existing_subnet_id",
    advanced=True,
    help="One or more already existing VCN subnet IDs (format: 'ocid1.subnet....'). "
         "All specified VCN subnets will be configured as Network entities within the Bright cluster "
         "(i.e. it will be possible to create cloud nodes on them). "
         "Subnets not specified at cluster-create time can be added later on by manually "
         "creating new Network entities. "
         "The first specified VCN subnet will be the one hosting the head node (you cannot change this later). "
         "Compute nodes can be assigned to a different subnet by changing the Network entity of their NIC; this should "
         "be done before first-time powering on (creating) a compute node instance.",
    help_varname="SUBNET_ID"
)
config_ns.add_parameter(
    "oci_availability_domain",
    env="OCI_AVAILABILITY_DOMAIN",
    help=(
        "Name of the OCI availability domain in which the subnet and all of the instances"
        " will be created. When not specified, a random availability domain will be used."
        " Useful when your chosen VM type is not available in all availability domains."
    )
)
config_ns.override_imported_parameter(
    "ssh_pub_key_path",
    validation=lambda p, c: validate_ssh_pub_key(p, c, allowed_types={"RSA": 2048})
)
config_ns.add_switch_parameter(
    "use_principal_authentication",
    help="Use instance principal authentication to manage the compute nodes, "
         "instead of copying and using the OCI key (required when using an encrypted key)"
)
config_ns.add_parameter(
    "node_shape",
    advanced=True,
    help="Name of the shape to use when creating new compute nodes.",
    default="VM.Standard.E4.Flex",
)

config_ns.add_parameter(
    "node_image_id",
    help="OCID of the image to use when creating new nodes.",
    default=None,
)

config_ns.add_parameter(
    "node_number_cpus",
    advanced=True,
    help="Number of CPUs for each node. If not set then the default value from the node shape will be used.",
    help_varname="NODE_NUMBER_CPUS",
    type=int,
)
config_ns.add_parameter(
    "node_memory_size",
    advanced=True,
    help="Size of the memory allocated for the compute nodes in GB. If not set then the default value from the node "
         "shape will be used.",
    help_varname="NODE_MEMORY_SIZE_IN_GB",
    type=int,
)
config_ns.add_parameter(
    "node_root_volume_size",
    default=50,
    help="Node root disk size in GB.",
    type=int,
    #
    # Ref: https://support.oracle.com/knowledge/Oracle%20Cloud/2683441_1.html
    validation=[may_not_equal_none, number_must_be_between(50, 32768)],
)
config_ns.add_switch_parameter(
    "node_use_cluster_network",
    help="Create nodes in the same Cluster Network. This parameter is needed for RDMA support.",
    # TODO: If enabled, we should validate node shape is at least bare-metal.
    # FIXME: Enable by default? If so, we should also and update defaults for mem/cpu.
)
config_ns.add_parameter(
    "instance_configuration_id",
    advanced=True,
    help="ID of instance configuration which will be applied to the instance pool used for compute nodes.",
)
config_ns.add_switch_parameter(
    "accept_oci_terms",
    advanced=True,
    help="Accept the OCI terms and conditions that are associated with the images usage."
)

headnodecreate_ns = ConfigNamespace("oci.headnode.create")
headnodecreate_ns.add_parameter(
    "head_node_image",
    help="Image name or OCID to be used for the head node",
)

headnodecreate_ns.add_parameter(
    "head_node_shape",
    help="Name of the shape to use when creating the head node",
    default="VM.Standard.E4.Flex",
    type=str
)
headnodecreate_ns.add_parameter(
    "head_node_number_cpus",
    default=2,
    help="Number of vCPUs allocated for the headnode virtual machine",
    help_varname="HEADNODE_NUMBER_CPUS",
    validation=may_not_equal_none,
    type=int
)
headnodecreate_ns.add_parameter(
    "head_node_memory_size",
    default=4,
    help="Size of the memory allocated for the headnode virtual machine",
    help_varname="HEADNODE_MEMORY_SIZE_IN_GB",
    validation=[may_not_equal_none],
    type=int
)
#
# This setting has this name so it has the same naming format as 'head_node_root_volume_size', defined
# in clusterondemand/configuration.py. Accepted values are per Oracle; ref:
#
# https://docs.oracle.com/en-us/iaas/tools/python/latest/api/core/models/oci.core.models.InstanceSourceViaImageDetails.html#oci.core.models.InstanceSourceViaImageDetails.boot_volume_vpus_per_gb
headnodecreate_ns.add_parameter(
    "head_node_root_volume_vpus",
    default=10,
    help="Number of Volume Peformance Units (VPUs) per GB to apply to the head node's boot volume.",
    help_varname="HEADNODE_ROOT_VOLUME_VPUS",
    validation=[number_must_be_between(10, 120), must_be_multiple_of(10)],
    advanced=True,
    type=int
)
headnodecreate_ns.add_enumeration_parameter(
    "head_node_tags",
    default=[],
    help=("List of tags to be added to the head node "
          "(e.g. --head-node-tags tag1=value tag2=value)"),
    parser=utils.parse_assignment,
    serializer=lambda val: "{}={}".format(*val)
)
config_ns.import_namespace(headnodecreate_ns)


def run_command():
    ClusterCreate().run()


class ClusterCreate(ClusterCommand):
    IMAGE_API_HASH_TAG = "BCM_API_HASH"

    def __init__(self):
        super().__init__()

    def _validate_params(self):
        self._validate_cluster_name()
        self._validate_access_credentials()
        self._validate_availability_domain()
        self._validate_shape()
        self._validate_head_node_ip()

    def _generate_cloud_config(self, subnet_id: str, private_subnet_id: str, node_nsg_id: str) -> str:
        node_instance_configuration_id = ""
        if config["instance_configuration_id"]:
            node_instance_configuration_id = config["instance_configuration_id"]
            log.info(f"Using supplied instance configuration ID '{node_instance_configuration_id}'")

        subnet = self._get_subnet(subnet_id)
        private_subnet = self._get_subnet(private_subnet_id) if private_subnet_id else None
        vcn = self._get_vcn(subnet.vcn_id)

        bright_setup = generate_bright_setup(
            config["name"],
            self.node_image_id,
            vcn.cidr_block,
            subnet_id,
            subnet.cidr_block,
            private_subnet_id,
            private_subnet.cidr_block if private_subnet else "",
            node_nsg_id,
            node_instance_configuration_id,
            get_oci_key_content(),
        )

        cloud_config = build_cloud_config(bright_setup, config["version"], "ubuntu")
        formatted_cloud_config = "#cloud-config\n" + yaml.safe_dump(cloud_config.to_dict())

        cloud_init_script = base64.b64encode(formatted_cloud_config.encode()).decode("utf-8")

        return cloud_init_script

    @staticmethod
    def _readfile(filename):
        filepath = pathlib.Path(filename)
        with open(filepath.expanduser().resolve(), encoding="UTF-8") as filehandle:
            file_contents = filehandle.read().rstrip()

        return file_contents

    def _generate_cluster_name(self, cluster_name: str) -> str:
        #
        # Broken out as a separate function in case we need to add more functionality; this mirrors
        # other module(s)
        return f"{cluster_name}-01"

    def _get_vcn_name_for_cluster(self, cluster_name: str) -> str:
        return f"{config['fixed_cluster_prefix']}{cluster_name}"

    def _create_vcn(self, compartment_id: str, cluster_name: str, cidr_blocks: list[str]) -> oci.core.models.Vcn:
        """
        Creates VCN and IGW in the provided compartment
        """
        try:
            # DNS labels have a max of 15 chars
            dns_label = re.sub("[^A-Za-z0-9]+", "", cluster_name)[:14]
            log.debug("Set DNS label '%s' based on cluster name '%s'", dns_label, cluster_name)

            vcn_name = self._get_vcn_name_for_cluster(cluster_name)

            vcn_details = oci.core.models.CreateVcnDetails(
                compartment_id=compartment_id,
                display_name=vcn_name,
                cidr_blocks=cidr_blocks,
                dns_label=dns_label,
                freeform_tags=self._generate_freeform_tags_for("Virtual Cloud Network"),
            )

            vcn = self.client.network.create_vcn(vcn_details)

            igw_details = oci.core.models.CreateInternetGatewayDetails(
                compartment_id=compartment_id,
                vcn_id=vcn.id,
                # display_name="bright-computing-cluster-igw",
                display_name=cluster_name,
                is_enabled=True,
                freeform_tags=self._generate_freeform_tags_for("Internet Gateway"),
            )

            igw = self.client.network.create_internet_gateway(igw_details)
            route_rule = oci.core.models.RouteRule(
                cidr_block=None,
                destination="0.0.0.0/0",
                # destination_type="CIDR_BLOCK",
                destination_type=oci.core.models.RouteRule.DESTINATION_TYPE_CIDR_BLOCK,
                network_entity_id=igw.id
            )

            self.client.network.add_route_table_rule(vcn.default_route_table_id, route_rule)

            return vcn

        except ServiceError as error:
            if error.code == "NotAuthorizedOrNotFound":
                raise UserReportableException(
                    "Unable to create VCN."
                    " Either the parent Compartment doesn't exist or user permissions are not sufficient."
                    f" OCI error message: {error.message}"
                ) from error

            raise CODException(error.message) from error

    def _create_security_groups(
            self,
            compartment_id: str,
            vcn_id: str,
            cluster_name: str,
            inbound_rules: list[InboundTrafficRule],
            ingress_icmp_cidr: netaddr.IPNetwork) -> list[oci.core.models.NetworkSecurityGroup]:
        """
        Creates security groups for head and worker nodes and adds all provided inbound_rules
        to the head node security group
        """

        try:
            head_nsg_details = oci.core.models.CreateNetworkSecurityGroupDetails(
                display_name=f"Bright {cluster_name}-headnode",
                compartment_id=compartment_id,
                vcn_id=vcn_id,
                freeform_tags=self._generate_freeform_tags_for("NSG"),
            )

            inbound_traffic_rules = InboundTrafficRule.process_inbound_rules(inbound_rules)
            security_rules = []

            if ingress_icmp_cidr:
                security_rules = [
                    oci.core.models.AddSecurityRuleDetails(
                        direction=oci.core.models.AddSecurityRuleDetails.DIRECTION_INGRESS,
                        is_stateless=False,
                        protocol=str(socket.getprotobyname("icmp")),
                        source=str(ingress_icmp_cidr),
                        source_type=oci.core.models.AddSecurityRuleDetails.SOURCE_TYPE_CIDR_BLOCK
                    )
                ]

            for inbound_rule in inbound_traffic_rules:
                security_rules.append(
                    oci.core.models.AddSecurityRuleDetails(
                        direction=oci.core.models.AddSecurityRuleDetails.DIRECTION_INGRESS,
                        is_stateless=False,
                        protocol=str(socket.getprotobyname(inbound_rule.protocol)),
                        source=inbound_rule.src_cidr,
                        source_type=oci.core.models.AddSecurityRuleDetails.SOURCE_TYPE_CIDR_BLOCK,
                        tcp_options=oci.core.models.TcpOptions(
                            destination_port_range=oci.core.models.PortRange(
                                min=int(inbound_rule.dst_first_port),
                                max=int(inbound_rule.dst_last_port))))
                )

            nsg_rules_details = oci.core.models.AddNetworkSecurityGroupSecurityRulesDetails(
                security_rules=security_rules)

            return self.client.network.create_security_group(head_nsg_details, nsg_rules_details)

        except ServiceError as error:
            if error.code == "NotAuthorizedOrNotFound":
                raise UserReportableException(
                    "Unable to create Network Security Group."
                    " Either the parent Compartment or VCN doesn't exist or user permissions are not sufficient."
                    f" OCI error message: {error.message}"
                ) from error

            raise CODException(error.message) from error

    def _create_subnet(
            self,
            vcn_id: str,
            compartment_id: str,
            subnet_name: str,
            cidr_block: str,
            route_table_id: str | None = None) -> oci.core.models.Subnet:
        try:
            subnet_details = oci.core.models.CreateSubnetDetails(
                vcn_id=vcn_id,
                compartment_id=compartment_id,
                route_table_id=route_table_id,
                display_name=subnet_name,
                dns_label=None,
                cidr_block=cidr_block,
                freeform_tags=self._generate_freeform_tags_for("Subnet"),
            )
            return self.client.network.create_subnet(subnet_details)

        except ServiceError as error:
            if error.code == "NotAuthorizedOrNotFound":
                raise UserReportableException(
                    f"Unable to create {subnet_name} subnet."
                    " Either the provided VCN doesn't exist or user permissions are not sufficient."
                    f" OCI error message: {error.message}"
                ) from error

            raise CODException(error.message) from error

    def _create_private_subnet(
            self,
            vcn_id: str,
            compartment_id: str,
            cluster_name: str,
            cidr_block: str) -> oci.core.models.Subnet:
        ngw_details = oci.core.models.CreateNatGatewayDetails(
            compartment_id=compartment_id,
            vcn_id=vcn_id,
            display_name=cluster_name,
            freeform_tags=self._generate_freeform_tags_for("NAT Gateway"),
        )

        ngw = self.client.network.create_nat_gateway(ngw_details)

        route_table_details = oci.core.models.CreateRouteTableDetails(
            compartment_id=compartment_id,
            vcn_id=vcn_id,
            display_name=f"{cluster_name}-private",
            freeform_tags=self._generate_freeform_tags_for("Route Table"),
            route_rules=[
                oci.core.models.RouteRule(
                    cidr_block=None,
                    destination="0.0.0.0/0",
                    destination_type=oci.core.models.RouteRule.DESTINATION_TYPE_CIDR_BLOCK,
                    network_entity_id=ngw.id
                ),
            ],
        )

        route_table = self.client.network.create_route_table(route_table_details)
        subnet = self._create_subnet(
            vcn_id,
            compartment_id,
            f"{cluster_name}-private",
            cidr_block,
            route_table_id=route_table.id,
        )
        return subnet

    def _get_head_node_name(self, cluster_name: str) -> str:
        return f"{cluster_name}-head-node"

    def _create_head_node(
            self,
            cluster_name: str,
            compartment_id: str,
            subnet_id: str,
            private_subnet_id: str,
            availability_domain_name: str,
            shape_name: str,
            head_nsg_id: str,
            node_nsg_id: str,
    ) -> oci.core.models.Instance:
        """
        Launches head node with all the necessary configuration
        """

        shape_name = config["head_node_shape"]
        shape = self.client.compute.get_shape(
            shape_name,
            availability_domain_name,
            compartment_id
        )

        #
        # Passing memory/CPU options to Bare Metal ("BM") instances is not necessary. You can do it, but
        # if they don't match the values of the shape the creation will throw an error. Since the user
        # has effectively selected memory/CPU by selecting the shape type, only use these values when
        # creating a VM head node.
        #
        # Another way to do this would be to not set defaults for CPU/memory; then we could throw an error
        # during the config parsing stage if the user specified a BM instance type with CPU and/or memory settings
        shape_config = None
        if shape_name.startswith("VM."):
            shape_config = self.client.compute.get_shape_config(
                config["head_node_memory_size"],
                config["head_node_number_cpus"],
            )

        cloud_init_script = self._generate_cloud_config(
            subnet_id,
            private_subnet_id,
            node_nsg_id,
        )

        head_node_name = self._get_head_node_name(cluster_name)

        instance_metadata = {
            "user_data": cloud_init_script,
        }

        if config["ssh_pub_key_path"]:
            instance_metadata["ssh_authorized_keys"] = self._readfile(config["ssh_pub_key_path"])

        head_node_tags = dict(config["head_node_tags"])
        head_node_tags[IMAGE_NAME_TAG] = self.head_node_image.name
        # timeformat same as oci portal, 2023-07-03T09:04:52.555Z (Z for UTC)
        head_node_tags[IMAGE_CREATED_TIME_TAG] = \
            self.head_node_image.created_at.isoformat(timespec="milliseconds") + "Z"

        instance_source_via_image_details = oci.core.models.InstanceSourceViaImageDetails(
            image_id=self.head_node_image_id,
            boot_volume_size_in_gbs=config["head_node_root_volume_size"],
            boot_volume_vpus_per_gb=config["head_node_root_volume_vpus"],
        )

        create_vnic_details = oci.core.models.CreateVnicDetails(
            subnet_id=subnet_id,
            nsg_ids=[head_nsg_id],
            private_ip=str(config["head_node_ip"]) if config["head_node_ip"] else None,
        )

        instance_options = self._get_instance_configuration_options(are_legacy_imds_endpoints_disabled=True)

        head_node_details = oci.core.models.LaunchInstanceDetails(
            availability_domain=availability_domain_name,
            compartment_id=compartment_id,
            create_vnic_details=create_vnic_details,
            display_name=head_node_name,
            instance_options=instance_options,
            metadata=instance_metadata,
            shape=shape.shape,
            shape_config=shape_config,
            # extended_metadata=instance_extended_metadata,
            source_details=instance_source_via_image_details,
            freeform_tags=head_node_tags | self._generate_freeform_tags_for("Head Node"),
        )

        launched_instance = self.client.compute.launch_instance(
            head_node_details
        )
        return launched_instance

    def _get_instance_configuration_options(
            self,
            are_legacy_imds_endpoints_disabled: bool = True,
    ) -> oci.core.models.InstanceConfigurationInstanceOptions:

        #
        # If set to True, disables legacy on-instance v1 metadata endpoint
        # ref: https://docs.oracle.com/en-us/iaas/Content/Compute/Tasks/gettingmetadata.htm
        return oci.core.models.InstanceOptions(
            are_legacy_imds_endpoints_disabled=are_legacy_imds_endpoints_disabled,
        )

    def _create_cluster(self, compute_cid: str, networking_cid: str):
        head_node_shape = config["head_node_shape"]

        if config["existing_subnet_id"]:
            subnet = self._get_subnet(config["existing_subnet_id"][0])
            vcn_id = subnet.vcn_id
            subnet_id = subnet.id
            log.info("Using existing public subnet: %r", subnet.display_name)

            private_subnet_id = ""
            if len(config["existing_subnet_id"]) == 2:
                private_subnet = self._get_subnet(config["existing_subnet_id"][1])
                private_subnet_id = private_subnet.id
                log.info("Using existing private subnet: %r", private_subnet.display_name)
            elif len(config["existing_subnet_id"]) > 2:
                raise CODException(
                    "When creating a COD-OCI cluster in an already existing VCN, you can specify only 1 or 2 "
                    "existing VCN subnets. If 1 subnet is specified, the head node and all the initial cnode "
                    "definitions are defined on that subnet. If 2 subnets are specified, the first one is used "
                    "for the head node, the second is used for all initial cnode definitions. "
                    "If you have more than two subnets in your existing VCN, and you don't need to use them "
                    "as part of this BCM cluster, do not include them on the CLI. You can configure additional VCN "
                    "subnets in BCM admin interface at any point later on after having created the cluster."
                )
        else:
            cluster_name = self._generate_cluster_name(config["name"])

            log.info("Creating VCN")
            vcn = self._create_vcn(networking_cid, cluster_name, [str(config["vcn_cidr"])])
            vcn_id = vcn.id
            log.debug("Created VCN: %r (%s)", vcn.display_name, vcn_id)
            log.info("Creating public subnet")
            subnet = self._create_subnet(vcn.id, networking_cid, f"{cluster_name}-public", str(config["subnet_cidr"]))
            subnet_id = subnet.id
            log.debug("Created public subnet: %r (%s)", subnet.display_name, subnet_id)
            log.info("Creating private subnet")
            private_subnet = self._create_private_subnet(vcn.id, networking_cid, cluster_name,
                                                         str(config["private_subnet_cidr"]))
            private_subnet_id = private_subnet.id
            log.debug("Created private subnet: %r (%s)", private_subnet.display_name, private_subnet_id)

        if config["head_node_nsg_id"] and config["node_nsg_id"]:
            head_nsg_id = config["head_node_nsg_id"]
            node_nsg_id = config["node_nsg_id"]
            log.info("Using existing head NSG: %r", head_nsg_id)
            log.info("Using existing node NSG: %r", node_nsg_id)
        else:
            log.info("Creating network security groups")
            head_nsg, node_nsg = self._create_security_groups(
                networking_cid,
                vcn_id,
                config["name"],
                config["inbound_rule"],
                config["ingress_icmp"],
            )
            head_nsg_id = head_nsg.id
            node_nsg_id = node_nsg.id
            log.debug("Created head NSG: '%s' (%s)", head_nsg.display_name, head_nsg_id)
            log.debug("Created node NSG: '%s' (%s)", node_nsg.display_name, node_nsg_id)

        log.info("Creating head node")
        head_node = self._create_head_node(
            config["name"],
            compute_cid,
            subnet_id,
            private_subnet_id,
            self.availability_domain_name,
            head_node_shape,
            head_nsg_id,
            node_nsg_id,
        )
        head_node_ip = self._get_instance_primary_ip(head_node)

        # FIXME: unhardcode the bcm version below once CM-43586 is merged.
        wait_for_cluster_to_be_ready(config, head_node_ip, "trunk")

        generator = OCISummaryGenerator(
            config,
            SummaryType.Overview,
            instance_id=head_node.id,
            public_ip=head_node_ip,
            node_image_id=self.node_image_id
        )
        generator.print_summary(log.info)

    def _rollback_cluster(self, cluster_name: str, compute_cid: str, networking_cid: str):
        #
        # There's a race condition here; despite the API calls to create the objects having returned, when
        # the various delete_* calls run queries-by-tag to find the objects, it may not (yet) find any.
        # A 5 second pause seems to be enough to let the OCI backend settle so that our queries work; setting
        # it to 10 seconds as a bit of an extra buffer. This is purely a stop-gap;  the correct solution is
        # implement some polling logic.
        #
        # Worst case, the user can simply run "cluster delete" to nuke everything.
        time.sleep(10)

        # FIXME improve this to be able to delete different object types from different
        # FIXME compartments (e.g. VCNs from a "networking" compartment, instances from an "instance"
        # FIXME compartment, and so on. For now, keep them separate since we get that kinda-sorta for free.
        cluster_delete = ClusterDelete()
        cluster_delete.delete_cluster(Cluster(cluster_name=cluster_name), compute_cid, networking_cid)

    def _ask_accept_agreements(self, head_node_image: CODException) -> None:
        head_agreements: list[oci.marketplace.models.AgreementSummary] = []
        if isinstance(head_node_image, CommunityAppImage):
            publication_id = head_node_image.uuid
            head_agreements = self.client.marketplace.get_image_agreements_to_accept(publication_id,
                                                                                     self.compute_cid)
            if head_agreements:
                head_agreements_text = "\n".join([f"- {agreement.content_url}" for agreement in head_agreements])
            else:
                log.debug(f"Head node image community application {head_node_image.name} agreements have already "
                          "been accepted.")
                head_agreements_text = "(already accepted)"
        else:
            head_agreements_text = "(not applicable)"

        # Head node image may have different terms in theory, so let's always show hardcoded terms for compute node.
        node_agreements_text = "\n".join([
            # The URL is a Pre-Authenticated Request to "community-application" bucket with very long expiration date.
            "- https://axvrabcwoa8f.objectstorage.eu-amsterdam-1.oci.customer-oci.com/p/-WWxiTlRRZ9YFdc_AAoroPPm3kFHN4RntNxj4dVlUI66fSq0875hgigneyDkRy3B/n/axvrabcwoa8f/b/community-application/o/eula.html",  # noqa: E501
            "- https://cloudmarketplace.oracle.com/marketplace/content?contentId=50511634&render=inline",
            "- https://www.oracle.com/legal/privacy/privacy-policy.html",
        ])

        prompt = (
            "Oracle Cloud Infrastructure (OCI) requires acceptance of terms & conditions associated with relevant "
            "images whenever a new version of these images is made available. The following terms & conditions / end "
            "user license agreements must be accepted in order to use this software:\n\n"
            f"Head node terms:\n{head_agreements_text}\n\nCompute node terms:\n{node_agreements_text}\n\n"
            "Do you grant permission for Bright Cluster Manager to accept the required end user license agreements "
            "and terms & conditions on your behalf when creating machine instances in OCI?"
        )

        if config["accept_oci_terms"]:
            log.debug("User accepted the OCI image usage terms through the configuration.")
        elif not utils.confirm(prompt, "accept_oci_terms"):
            raise UserReportableException("Cannot create a cluster using without accepting the agreements")

        if head_agreements:
            self.client.marketplace.accept_image_agreements(
                self.compute_cid,
                publication_id,
                [agreement.id for agreement in head_agreements]
            )

    def run(self):
        compute_cid = self.compute_cid
        networking_cid = self.networking_cid

        self._validate_params()

        if config["existing_subnet_id"] and not config.is_item_set_from_defaults("vcn_cidr"):
            raise ValidationException("May not pass '--existing-subnet-id' while also passing '--vcn-cidr'")

        # Ensure there is no existing cluster with the same name
        existing_clusters = [
            c.freeform_tags.get(CLUSTER_NAME_TAG) for c in get_head_node_list(
                client=self.client, compute_cid=self.compute_cid
            )
            if c.lifecycle_state != Instance.LIFECYCLE_STATE_TERMINATED
        ]
        if config["name"] in existing_clusters:
            raise UserReportableException(
                f"A cluster with the name '{config['name']}' already exists, please choose a different cluster name."
            )

        self.head_node_image = OCIImageSource.pick_head_node_image_using_options(config)
        if not self.head_node_image.version and config["run_cm_bright_setup"]:
            log.warning(
                f"Using custom image: {self.head_node_image.name} ({self.head_node_image.uuid}) with parameter "
                "run_cm_bright_setup set to 'yes'. Probably it was set by mistake because a custom image might not "
                "have necessary files to run cm-bright-setup. Consider using --run-cm-bright-setup=no."
            )

        if isinstance(self.head_node_image, CommunityAppImage):
            self.head_node_image_id = self.head_node_image.custom_image_id
        else:
            self.head_node_image_id = self.head_node_image.uuid

        self._ask_accept_agreements(self.head_node_image)

        node_image = None
        self.node_image_id = config["node_image_id"]
        if self.node_image_id:
            node_image = make_cod_image_from_ocid(self.client, self.node_image_id, allow_custom_images=True)

        def print_overview():
            head_node_definition = NodeDefinition(count=1,
                                                  flavor=config["head_node_shape"],
                                                  )
            node_definition = NodeDefinition(count=config["nodes"],
                                             flavor=config["node_shape"],
                                             )
            compartment = self.client.identity.get_compartment(compute_cid)
            generator = OCISummaryGenerator(config,
                                            SummaryType.Proposal,
                                            config["oci_region"],
                                            head_node_definition,
                                            node_definition,
                                            self.head_node_image,
                                            node_image,
                                            self.head_node_image_id,
                                            self.node_image_id,
                                            compartment_name=compartment.name,
                                            )
            generator.print_summary(log.info)

        print_overview()

        if config["ask_to_confirm_cluster_creation"]:
            utils.confirm_cluster_creation()

        if config["dry_run"]:
            log.info("Running in dry-run mode. Cluster will not be created.")
            return

        try:
            self._create_cluster(compute_cid, networking_cid)
        except Exception as error:
            if not isinstance(error, CODException):
                message = error.message if hasattr(error, "message") else str(error)
                cod_error = CODException(message)
            else:
                cod_error = error

            log.error("The following error occurred while creating the cluster")
            log.error(error)

            if config["on_error"] == "cleanup":
                log.info("Removing created resources...")
                cluster_name = config["name"]
                self._rollback_cluster(cluster_name, compute_cid, networking_cid)
            else:
                log.info("Failed environment was kept and will have to be deleted manually.")

            raise cod_error
