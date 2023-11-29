
########
# Copyright (c) 2014-2022 Cloudify Platform Ltd. All rights reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import yaml

deprecated_node_types = {
    'cloudify.azure.nodes.resources.Azure':
        'cloudify.nodes.azure.resources.Azure',
    'cloudify.azure.nodes.compute.ManagedCluster':
        'cloudify.nodes.azure.compute.ManagedCluster',
    'cloudify.azure.nodes.compute.ContainerService':
        'cloudify.nodes.azure.compute.ContainerService',
    'cloudify.azure.nodes.network.LoadBalancer.Probe':
        'cloudify.nodes.azure.network.LoadBalancer.Probe',
    'cloudify.azure.nodes.network.LoadBalancer.BackendAddressPool':
        'cloudify.nodes.azure.network.LoadBalancer.BackendAddressPool',
    'cloudify.azure.nodes.network.LoadBalancer.IncomingNATRule':
        'cloudify.nodes.azure.network.LoadBalancer.IncomingNATRule',
    'cloudify.azure.nodes.network.LoadBalancer.Rule':
        'cloudify.nodes.azure.network.LoadBalancer.Rule',
    'cloudify.azure.nodes.network.LoadBalancer':
        'cloudify.nodes.azure.network.LoadBalancer',
    'cloudify.azure.nodes.compute.VirtualMachineExtension':
        'cloudify.nodes.azure.compute.VirtualMachineExtension',
    'cloudify.azure.nodes.PublishingUser':
        'cloudify.nodes.azure.PublishingUser',
    'cloudify.azure.nodes.WebApp':
        'cloudify.nodes.azure.WebApp',
    'cloudify.azure.nodes.Plan':
        'cloudify.nodes.azure.Plan',
    'cloudify.azure.nodes.compute.WindowsVirtualMachine':
        'cloudify.nodes.azure.compute.WindowsVirtualMachine',
    'cloudify.azure.nodes.compute.AvailabilitySet':
        'cloudify.nodes.azure.compute.AvailabilitySet',
    'cloudify.azure.nodes.network.Route':
        'cloudify.nodes.azure.network.Route',
    'cloudify.azure.nodes.network.NetworkSecurityRule':
        'cloudify.nodes.azure.network.NetworkSecurityRule',
    'cloudify.azure.nodes.network.RouteTable':
        'cloudify.nodes.azure.network.RouteTable',
    'cloudify.azure.nodes.network.Subnet':
        'cloudify.nodes.azure.network.Subnet',
    'cloudify.azure.nodes.compute.VirtualMachine':
        'cloudify.nodes.azure.compute.VirtualMachine',
    'cloudify.azure.nodes.network.NetworkInterfaceCard':
        'cloudify.nodes.azure.network.NetworkInterfaceCard',
    'cloudify.azure.nodes.network.NetworkSecurityGroup':
        'cloudify.nodes.azure.network.NetworkSecurityGroup',
    'cloudify.azure.nodes.network.IPConfiguration':
        'cloudify.nodes.azure.network.IPConfiguration',
    'cloudify.azure.nodes.network.VirtualNetwork':
        'cloudify.nodes.azure.network.VirtualNetwork',
    'cloudify.azure.nodes.network.PublicIPAddress':
        'cloudify.nodes.azure.network.PublicIPAddress',
    'cloudify.azure.nodes.ResourceGroup':
        'cloudify.nodes.azure.ResourceGroup',
    'cloudify.azure.nodes.storage.StorageAccount':
        'cloudify.nodes.azure.storage.StorageAccount',
    'cloudify.azure.nodes.storage.DataDisk':
        'cloudify.nodes.azure.storage.DataDisk',
    'cloudify.azure.nodes.storage.FileShare':
        'cloudify.nodes.azure.storage.FileShare',
    'cloudify.azure.nodes.storage.VirtualNetwork':
        'cloudify.nodes.azure.storage.VirtualNetwork',
    'cloudify.azure.nodes.storage.NetworkSecurityGroup':
        'cloudify.nodes.azure.storage.NetworkSecurityGroup',
    'cloudify.azure.nodes.storage.NetworkSecurityRule':
        'cloudify.nodes.azure.storage.NetworkSecurityRule',
    'cloudify.azure.nodes.storage.RouteTable':
        'cloudify.nodes.azure.storage.RouteTable',
    'cloudify.azure.nodes.storage.Route':
        'cloudify.nodes.azure.storage.Route',
    'cloudify.azure.nodes.storage.IPConfiguration':
        'cloudify.nodes.azure.storage.IPConfiguration',
    'cloudify.azure.nodes.storage.PublicIPAddress':
        'cloudify.nodes.azure.storage.PublicIPAddress',
    'cloudify.azure.nodes.storage.AvailabilitySet':
        'cloudify.nodes.azure.storage.AvailabilitySet',
    'cloudify.azure.nodes.storage.VirtualMachine':
        'cloudify.nodes.azure.storage.VirtualMachine',
    'cloudify.azure.nodes.storage.WindowsVirtualMachine':
        'cloudify.nodes.azure.storage.WindowsVirtualMachine',
    'cloudify.azure.nodes.storage.VirtualMachineExtension':
        'cloudify.nodes.azure.storage.VirtualMachineExtension',
    'cloudify.azure.nodes.storage.LoadBalancer':
        'cloudify.nodes.azure.storage.LoadBalancer',
    'cloudify.azure.nodes.storage.BackendAddressPool':
        'cloudify.nodes.azure.storage.BackendAddressPool',
    'cloudify.azure.nodes.storage.Probe':
        'cloudify.nodes.azure.storage.Probe',
    'cloudify.azure.nodes.storage.IncomingNATRule':
        'cloudify.nodes.azure.storage.IncomingNATRule',
    'cloudify.azure.nodes.storage.Rule':
        'cloudify.nodes.azure.storage.Rule',
    'cloudify.azure.nodes.storage.ContainerService':
        'cloudify.nodes.azure.storage.ContainerService',
    'cloudify.azure.nodes.storage.Plan':
        'cloudify.nodes.azure.storage.Plan',
    'cloudify.azure.nodes.storage.WebApp':
        'cloudify.nodes.azure.storage.WebApp',
    'cloudify.azure.nodes.storage.PublishingUser':
        'cloudify.nodes.azure.storage.PublishingUser',
    'cloudify.azure.nodes.storage.ManagedCluster':
        'cloudify.nodes.azure.storage.ManagedCluster',
    'cloudify.azure.nodes.storage.Azure':
        'cloudify.nodes.azure.storage.Azure',

    'cloudify.openstack.nodes.Server':
        'cloudify.nodes.openstack.Server',
    'cloudify.openstack.nodes.WindowsServer':
        'cloudify.nodes.openstack.WindowsServer',
    'cloudify.openstack.nodes.KeyPair':
        'cloudify.nodes.openstack.KeyPair',
    'cloudify.openstack.nodes.Subnet':
        'cloudify.nodes.openstack.Subnet',
    'cloudify.openstack.nodes.SecurityGroup':
        'cloudify.nodes.openstack.SecurityGroup',
    'cloudify.openstack.nodes.Router':
        'cloudify.nodes.openstack.Router',
    'cloudify.openstack.nodes.Port':
        'cloudify.nodes.openstack.Port',
    'cloudify.openstack.nodes.Network':
        'cloudify.nodes.openstack.Network',
    'cloudify.openstack.nodes.FloatingIP':
        'cloudify.nodes.openstack.FloatingIP',
    'cloudify.openstack.nodes.RBACPolicy':
        'cloudify.nodes.openstack.RBACPolicy',
    'cloudify.openstack.nodes.Volume':
        'cloudify.nodes.openstack.Volume',
    'cloudify.openstack.nova_net.nodes.FloatingIP':
        'cloudify.nodes.openstack.FloatingIP',
    'cloudify.openstack.nova_net.nodes.SecurityGroup':
        'cloudify.nodes.openstack.SecurityGroup',
    'cloudify.openstack.nodes.Flavor':
        'cloudify.nodes.openstack.Flavor',
    'cloudify.openstack.nodes.Image':
        'cloudify.nodes.openstack.Image',
    'cloudify.openstack.nodes.Project':
        'cloudify.nodes.openstack.Project',
    'cloudify.openstack.nodes.User':
        'cloudify.nodes.openstack.User',
    'cloudify.openstack.nodes.HostAggregate':
        'cloudify.nodes.openstack.HostAggregate',
    'cloudify.openstack.nodes.ServerGroup':
        'cloudify.nodes.openstack.ServerGroup',
    'cloudify.openstack.nodes.Routes':
        'cloudify.nodes.openstack.Router',

    'cloudify.gcp.nodes.project':
        'cloudify.nodes.gcp.project',
    'cloudify.gcp.nodes.PolicyBinding':
        'cloudify.nodes.gcp.PolicyBinding',
    'cloudify.gcp.nodes.Instance':
        'cloudify.nodes.gcp.Instance',
    'cloudify.gcp.nodes.InstanceGroup':
        'cloudify.nodes.gcp.InstanceGroup',
    'cloudify.gcp.nodes.Volume':
        'cloudify.nodes.gcp.Volume',
    'cloudify.gcp.nodes.Snapshot':
        'cloudify.nodes.gcp.Snapshot',
    'cloudify.gcp.nodes.Network':
        'cloudify.nodes.gcp.Network',
    'cloudify.gcp.nodes.SubNetwork':
        'cloudify.nodes.gcp.SubNetwork',
    'cloudify.gcp.nodes.VPCNetworkPeering':
        'cloudify.nodes.gcp.VPCNetworkPeering',
    'cloudify.gcp.nodes.Route':
        'cloudify.nodes.gcp.Route',
    'cloudify.gcp.nodes.FirewallRule':
        'cloudify.nodes.gcp.FirewallRule',
    'cloudify.gcp.nodes.SecurityGroup':
        'cloudify.nodes.gcp.SecurityGroup',
    'cloudify.gcp.nodes.Access':
        'cloudify.nodes.gcp.Access',
    'cloudify.gcp.nodes.KeyPair':
        'cloudify.nodes.gcp.KeyPair',
    'cloudify.gcp.nodes.ExternalIP':
        'cloudify.nodes.gcp.ExternalIP',
    'cloudify.gcp.nodes.GlobalAddress':
        'cloudify.nodes.gcp.GlobalAddress',
    'cloudify.gcp.nodes.StaticIP':
        'cloudify.nodes.gcp.StaticIP',
    'cloudify.gcp.nodes.Address':
        'cloudify.nodes.gcp.Address',
    'cloudify.gcp.nodes.Imagev':
        'cloudify.nodes.gcp.Image',
    'cloudify.gcp.nodes.HealthCheck':
        'cloudify.nodes.gcp.HealthCheck',
    'cloudify.gcp.nodes.BackendService':
        'cloudify.nodes.gcp.BackendService',
    'cloudify.gcp.nodes.RegionBackendService':
        'cloudify.nodes.gcp.RegionBackendService',
    'cloudify.gcp.nodes.UrlMap':
        'cloudify.nodes.gcp.UrlMap',
    'cloudify.gcp.nodes.TargetProxy':
        'cloudify.nodes.gcp.TargetProxy',
    'cloudify.gcp.nodes.SslCertificate':
        'cloudify.nodes.gcp.SslCertificate',
    'cloudify.gcp.nodes.ForwardingRule':
        'cloudify.nodes.gcp.ForwardingRule',
    'cloudify.gcp.nodes.GlobalForwardingRule':
        'cloudify.nodes.gcp.GlobalForwardingRule',
    'cloudify.gcp.nodes.DNSZone':
        'cloudify.nodes.gcp.DNSZone',
    'cloudify.gcp.nodes.DNSRecord':
        'cloudify.nodes.gcp.DNSRecord',
    'cloudify.gcp.nodes.DNSAAAARecord':
        'cloudify.nodes.gcp.DNSAAAARecord',
    'cloudify.gcp.nodes.DNSMXRecord':
        'cloudify.nodes.gcp.DNSMXRecord',
    'cloudify.gcp.nodes.DNSNSRecord':
        'cloudify.nodes.gcp.DNSNSRecord',
    'cloudify.gcp.nodes.DNSTXTRecord':
        'cloudify.nodes.gcp.DNSTXTRecord',
    'cloudify.gcp.nodes.KubernetesCluster':
        'cloudify.nodes.gcp.KubernetesCluster',
    'cloudify.gcp.nodes.KubernetesNodePool':
        'cloudify.nodes.gcp.KubernetesNodePool',
    'cloudify.gcp.nodes.KubernetesClusterMonitoring':
        'cloudify.nodes.gcp.KubernetesClusterMonitoring',
    'cloudify.gcp.nodes.KubernetesClusterlegacyAbac':
        'cloudify.nodes.gcp.KubernetesClusterlegacyAbac',
    'cloudify.gcp.nodes.KubernetesClusterNetworkPolicy':
        'cloudify.nodes.gcp.KubernetesClusterNetworkPolicy',
    'cloudify.gcp.nodes.Topic':
        'cloudify.nodes.gcp.Topic',
    'cloudify.gcp.nodes.TopicPolicy':
        'cloudify.nodes.gcp.TopicPolicy',
    'cloudify.gcp.nodes.TopicMessage':
        'cloudify.nodes.gcp.TopicMessage',
    'cloudify.gcp.nodes.Subscription':
        'cloudify.nodes.gcp.Subscription',
    'cloudify.gcp.nodes.SubscriptionPolicy':
        'cloudify.nodes.gcp.SubscriptionPolicy',
    'cloudify.gcp.nodes.Acknowledge':
        'cloudify.nodes.gcp.Acknowledge',
    'cloudify.gcp.nodes.PullRequest':
        'cloudify.nodes.gcp.PullRequest',
    'cloudify.gcp.nodes.StackDriverGroup':
        'cloudify.nodes.gcp.StackDriverGroup',
    'cloudify.gcp.nodes.StackDriverTimeSeries':
        'cloudify.nodes.gcp.StackDriverTimeSeries',
    'cloudify.gcp.nodes.StackDriverUpTimeCheckConfig':
        'cloudify.nodes.gcp.StackDriverUpTimeCheckConfig',
    'cloudify.gcp.nodes.LoggingSink':
        'cloudify.nodes.gcp.LoggingSink',
    'cloudify.gcp.nodes.LoggingExclusion':
        'cloudify.nodes.gcp.LoggingExclusion',
    'cloudify.gcp.nodes.Logging.BillingAccounts.sinks':
        'cloudify.nodes.gcp.Logging.BillingAccounts.sinks',
    'cloudify.gcp.nodes.Logging.Folders.sinks':
        'cloudify.nodes.gcp.Logging.Folders.sinks',
    'cloudify.gcp.nodes.Logging.Organizations.sinks':
        'cloudify.nodes.gcp.Logging.Organizations.sinks',
    'cloudify.gcp.nodes.Logging.Projects.sinks':
        'cloudify.nodes.gcp.Logging.Projects.sinks',
    'cloudify.gcp.nodes.Logging.BillingAccounts.exclusions':
        'cloudify.nodes.gcp.Logging.BillingAccounts.exclusions',
    'cloudify.gcp.nodes.Logging.Folders.exclusions':
        'cloudify.nodes.gcp.Logging.Folders.exclusions',
    'cloudify.gcp.nodes.Logging.Organizations.exclusions':
        'cloudify.nodes.gcp.Logging.Organizations.exclusions',
    'cloudify.gcp.nodes.Logging.Organizatios.exclusions':
        'cloudify.nodes.gcp.Logging.Organizatios.exclusions',
    'cloudify.gcp.nodes.Logging.Projects.exclusions':
        'cloudify.nodes.gcp.Logging.Projects.exclusions',
    'cloudify.gcp.nodes.Logging.Projects.metrics':
        'cloudify.nodes.gcp.Logging.Projects.metrics',
    'cloudify.gcp.nodes.IAM.Role':
        'cloudify.nodes.gcp.IAM.Role',
    'cloudify.gcp.nodes.Gcp':
        'cloudify.nodes.gcp.Gcp',

    'cloudify.vsphere.nodes.Server':
        'cloudify.nodes.vsphere.Server',
    'cloudify.vsphere.nodes.WindowsServer':
        'cloudify.nodes.vsphere.WindowsServer',
    'cloudify.vsphere.nodes.Network':
        'cloudify.nodes.vsphere.Network',
    'cloudify.vsphere.nodes.Storage':
        'cloudify.nodes.vsphere.Storage',
    'cloudify.vsphere.nodes.IPPool':
        'cloudify.nodes.vsphere.IPPool',
    'cloudify.vsphere.nodes.CloudInitISO':
        'cloudify.nodes.vsphere.CloudInitISO',
    'cloudify.vsphere.nodes.Datacenter':
        'cloudify.nodes.vsphere.Datacenter',
    'cloudify.vsphere.nodes.Datastore':
        'cloudify.nodes.vsphere.Datastore',
    'cloudify.vsphere.nodes.Cluster':
        'cloudify.nodes.vsphere.Cluster',
    'cloudify.vsphere.nodes.ResourcePool':
        'cloudify.nodes.vsphere.ResourcePool',
    'cloudify.vsphere.nodes.VMFolder':
        'cloudify.nodes.vsphere.VMFolder',
    'cloudify.vsphere.nodes.Host':
        'cloudify.nodes.vsphere.Host',
    'cloudify.vsphere.nodes.ContentLibraryDeployment':
        'cloudify.nodes.vsphere.ContentLibraryDeployment',
    'cloudify.vsphere.nodes.NIC':
        'cloudify.nodes.vsphere.NIC',
    'cloudify.vsphere.nodes.SCSIController':
        'cloudify.nodes.vsphere.SCSIController'
}

deprecated_relationship_types = {
    'cloudify.azure.relationships.contained_in_resource_group':
        'cloudify.relationships.azure.contained_in_resource_group',
    'cloudify.azure.relationships.contained_in_storage_account':
        'cloudify.relationships.azure.contained_in_storage_account',
    'cloudify.azure.relationships.contained_in_virtual_network':
        'cloudify.relationships.azure.contained_in_virtual_network',
    'cloudify.azure.relationships.contained_in_network_security_group':
        'cloudify.relationships.azure.contained_in_network_security_group',
    'cloudify.azure.relationships.contained_in_route_table':
        'cloudify.relationships.azure.contained_in_route_table',
    'cloudify.azure.relationships.contained_in_load_balancer':
        'cloudify.relationships.azure.contained_in_load_balancer',
    'cloudify.azure.relationships.network_security_group_attached_to_subnet':
        'cloudify.relationships.azure.network_security_group_attached_to_subnet', # noqa
    'cloudify.azure.relationships.route_table_attached_to_subnet':
        'cloudify.relationships.azure.route_table_attached_to_subnet',
    'cloudify.azure.relationships.nic_connected_to_ip_configuration':
        'cloudify.relationships.azure.nic_connected_to_ip_configuration',
    'cloudify.azure.relationships.ip_configuration_connected_to_subnet':
        'cloudify.relationships.azure.ip_configuration_connected_to_subnet',
    'cloudify.azure.relationships.ip_configuration_connected_to_public_ip':
        'cloudify.relationships.azure.ip_configuration_connected_to_public_ip',
    'cloudify.azure.relationships.connected_to_storage_account':
        'cloudify.relationships.azure.connected_to_storage_account',
    'cloudify.azure.relationships.connected_to_data_disk':
        'cloudify.relationships.azure.connected_to_data_disk',
    'cloudify.azure.relationships.connected_to_nic':
        'cloudify.relationships.azure.connected_to_nic',
    'cloudify.azure.relationships.connected_to_availability_set':
        'cloudify.relationships.azure.connected_to_availability_set',
    'cloudify.azure.relationships.connected_to_ip_configuration':
        'cloudify.relationships.azure.connected_to_ip_configuration',
    'cloudify.azure.relationships.connected_to_lb_be_pool':
        'cloudify.relationships.azure.connected_to_lb_be_pool',
    'cloudify.azure.relationships.connected_to_lb_probe':
        'cloudify.relationships.azure.connected_to_lb_probe',
    'cloudify.azure.relationships.vmx_contained_in_vm':
        'cloudify.relationships.azure.vmx_contained_in_vm',
    'cloudify.azure.relationships.nic_connected_to_lb_be_pool':
        'cloudify.relationships.azure.nic_connected_to_lb_be_pool',
    'cloudify.azure.relationships.vm_connected_to_datadisk':
        'cloudify.relationships.azure.vm_connected_to_datadisk',
    'cloudify.azure.relationships.connected_to_aks_cluster':
        'cloudify.relationships.azure.connected_to_aks_cluster',

    'cloudify.openstack.server_connected_to_server_group':
        'cloudify.relationships.openstack.server_connected_to_server_group',
    'cloudify.openstack.server_connected_to_keypair':
        'cloudify.relationships.openstack.server_connected_to_keypair',
    'cloudify.openstack.server_connected_to_port':
        'cloudify.relationships.openstack.server_connected_to_port',
    'cloudify.openstack.server_connected_to_floating_ip':
        'cloudify.relationships.openstack.server_connected_to_floating_ip',
    'cloudify.openstack.server_connected_to_security_group':
        'cloudify.relationships.openstack.server_connected_to_security_group',
    'cloudify.openstack.port_connected_to_security_group':
        'cloudify.relationships.openstack.port_connected_to_security_group',
    'cloudify.openstack.port_connected_to_floating_ip':
        'cloudify.relationships.openstack.port_connected_to_floating_ip',
    'cloudify.openstack.port_connected_to_subnet':
        'cloudify.relationships.openstack.port_connected_to_subnet',
    'cloudify.openstack.subnet_connected_to_router':
        'cloudify.relationships.openstack.subnet_connected_to_router',
    'cloudify.openstack.volume_attached_to_server':
        'cloudify.relationships.openstack.volume_attached_to_server',
    'cloudify.openstack.route_connected_to_router':
        'cloudify.relationships.openstack.route_connected_to_router',
    'cloudify.openstack.rbac_policy_applied_to':
        'cloudify.relationships.openstack.rbac_policy_applied_to',

    'cloudify.gcp.relationships.instance_connected_to_security_group':
        'cloudify.relationships.gcp.instance_connected_to_security_group',
    'cloudify.gcp.relationships.instance_connected_to_ip':
        'cloudify.relationships.gcp.instance_connected_to_ip',
    'cloudify.gcp.relationships.instance_connected_to_keypair':
        'cloudify.relationships.gcp.instance_connected_to_keypair',
    'cloudify.gcp.relationships.instance_connected_to_disk':
        'cloudify.relationships.gcp.instance_connected_to_disk',
    'cloudify.gcp.relationships.instance_connected_to_instance_group':
        'cloudify.relationships.gcp.instance_connected_to_instance_group',
    'cloudify.gcp.relationships.uses_as_backend':
        'cloudify.relationships.gcp.uses_as_backend',
    'cloudify.gcp.relationships.uses_as_region_backend':
        'cloudify.relationships.gcp.uses_as_region_backend',
    'cloudify.gcp.relationships.contained_in_compute':
        'cloudify.relationships.gcp.contained_in_compute',
    'cloudify.gcp.relationships.dns_record_contained_in_zone':
        'cloudify.relationships.gcp.dns_record_contained_in_zone',
    'cloudify.gcp.relationships.dns_record_connected_to_instance':
        'cloudify.relationships.gcp.dns_record_connected_to_instance',
    'cloudify.gcp.relationships.dns_record_connected_to_ip':
        'cloudify.relationships.gcp.dns_record_connected_to_ip',
    'cloudify.gcp.relationships.contained_in_network':
        'cloudify.relationships.gcp.contained_in_network',
    'cloudify.gcp.relationships.instance_contained_in_network':
        'cloudify.relationships.gcp.instance_contained_in_network',
    'cloudify.gcp.relationships.forwarding_rule_connected_to_target_proxy':
        'cloudify.relationships.gcp.forwarding_rule_connected_to_target_proxy',
    'cloudify.gcp.relationships.vpn_network_peering_connected_to_network':
        'cloudify.relationships.gcp.vpn_network_peering_connected_to_network',
    'cloudify.gcp.relationships.subscription_connected_to_topic':
        'cloudify.relationships.gcp.subscription_connected_to_topic',
    'cloudify.gcp.relationships.instance_remove_access_config':
        'cloudify.relationships.gcp.instance_remove_access_config',

    'cloudify.vsphere.port_connected_to_network':
        'cloudify.relationships.vsphere.port_connected_to_network',
    'cloudify.vsphere.port_connected_to_server':
        'cloudify.relationships.vsphere.port_connected_to_server',
    'cloudify.vsphere.storage_connected_to_server':
        'cloudify.relationships.vsphere.storage_connected_to_server',
    'cloudify.vsphere.nic_connected_to_server':
        'cloudify.relationships.vsphere.nic_connected_to_server',
    'cloudify.vsphere.controller_connected_to_vm':
        'cloudify.relationships.vsphere.controller_connected_to_vm'
}

ACCEPTED_LIST_TYPES = (
    yaml.tokens.BlockEntryToken,
    yaml.tokens.FlowSequenceStartToken
)

TERRAFORM_TYPES = [
    'cloudify.nodes.terraform.Module',
]

AWS_TYPES = [
    'cloudify.nodes.aws.dynamodb.Table',
    'cloudify.nodes.aws.iam.Group',
    'cloudify.nodes.aws.iam.AccessKey',
    'cloudify.nodes.aws.iam.LoginProfile',
    'cloudify.nodes.aws.iam.User',
    'cloudify.nodes.aws.iam.Role',
    'cloudify.nodes.aws.iam.RolePolicy',
    'cloudify.nodes.aws.iam.InstanceProfile',
    'cloudify.nodes.aws.iam.Policy',
    'cloudify.nodes.aws.lambda.Function',
    'cloudify.nodes.aws.lambda.Invoke',
    'cloudify.nodes.aws.lambda.Permission',
    'cloudify.nodes.aws.rds.Instance',
    'cloudify.nodes.aws.rds.InstanceReadReplica',
    'cloudify.nodes.aws.rds.SubnetGroup',
    'cloudify.nodes.aws.rds.OptionGroup',
    'cloudify.nodes.aws.rds.Option',
    'cloudify.nodes.aws.rds.ParameterGroup',
    'cloudify.nodes.aws.rds.Parameter',
    'cloudify.nodes.aws.route53.HostedZone',
    'cloudify.nodes.aws.route53.RecordSet',
    'cloudify.nodes.aws.SQS.Queue',
    'cloudify.nodes.aws.SNS.Topic',
    'cloudify.nodes.aws.SNS.Subscription',
    'cloudify.nodes.aws.elb.LoadBalancer',
    'cloudify.nodes.aws.elb.Classic.LoadBalancer',
    'cloudify.nodes.aws.elb.Classic.HealthCheck',
    'cloudify.nodes.aws.elb.Listener',
    'cloudify.nodes.aws.elb.Classic.Listener',
    'cloudify.nodes.aws.elb.Rule',
    'cloudify.nodes.aws.elb.TargetGroup',
    'cloudify.nodes.aws.elb.Classic.Policy',
    'cloudify.nodes.aws.elb.Classic.Policy.Stickiness',
    'cloudify.nodes.aws.s3.BaseBucket',
    'cloudify.nodes.aws.s3.BaseBucketObject',
    'cloudify.nodes.aws.s3.Bucket',
    'cloudify.nodes.aws.s3.BucketPolicy',
    'cloudify.nodes.aws.s3.BucketLifecycleConfiguration',
    'cloudify.nodes.aws.s3.BucketTagging',
    'cloudify.nodes.aws.s3.BucketObject',
    'cloudify.nodes.aws.ec2.BaseType',
    'cloudify.nodes.aws.ec2.Vpc',
    'cloudify.nodes.aws.ec2.VpcPeering',
    'cloudify.nodes.aws.ec2.VpcPeeringRequest',
    'cloudify.nodes.aws.ec2.VpcPeeringAcceptRequest',
    'cloudify.nodes.aws.ec2.VpcPeeringRejectRequest',
    'cloudify.nodes.aws.ec2.Subnet',
    'cloudify.nodes.aws.ec2.SecurityGroup',
    'cloudify.nodes.aws.ec2.SecurityGroupRuleIngress',
    'cloudify.nodes.aws.ec2.SecurityGroupRuleEgress',
    'cloudify.nodes.aws.ec2.NATGateway',
    'cloudify.nodes.aws.ec2.Interface',
    'cloudify.nodes.aws.ec2.Instances',
    'cloudify.nodes.aws.ec2.SpotInstances',
    'cloudify.nodes.aws.ec2.SpotFleetRequest',
    'cloudify.nodes.aws.ec2.Keypair',
    'cloudify.nodes.aws.ec2.ElasticIP',
    'cloudify.nodes.aws.ec2.NetworkACL',
    'cloudify.nodes.aws.ec2.NetworkAclEntry',
    'cloudify.nodes.aws.ec2.DHCPOptions',
    'cloudify.nodes.aws.ec2.VPNGateway',
    'cloudify.nodes.aws.ec2.VPNConnection',
    'cloudify.nodes.aws.ec2.VPNConnectionRoute',
    'cloudify.nodes.aws.ec2.CustomerGateway',
    'cloudify.nodes.aws.ec2.InternetGateway',
    'cloudify.nodes.aws.ec2.TransitGateway',
    'cloudify.nodes.aws.ec2.TransitGatewayRouteTable',
    'cloudify.nodes.aws.ec2.TransitGatewayRoute',
    'cloudify.nodes.aws.ec2.RouteTable',
    'cloudify.nodes.aws.ec2.Route',
    'cloudify.nodes.aws.ec2.Image',
    'cloudify.nodes.aws.ec2.Tags',
    'cloudify.nodes.aws.ec2.EBSVolume',
    'cloudify.nodes.aws.ec2.EBSAttachment',
    'cloudify.nodes.aws.autoscaling.Group',
    'cloudify.nodes.aws.autoscaling.LaunchConfiguration',
    'cloudify.nodes.aws.autoscaling.Policy',
    'cloudify.nodes.aws.autoscaling.LifecycleHook',
    'cloudify.nodes.aws.autoscaling.NotificationConfiguration',
    'cloudify.nodes.aws.cloudwatch.Alarm',
    'cloudify.nodes.aws.cloudwatch.Rule',
    'cloudify.nodes.aws.cloudwatch.Event',
    'cloudify.nodes.aws.cloudwatch.Target',
    'cloudify.nodes.aws.efs.FileSystem',
    'cloudify.nodes.aws.efs.MountTarget',
    'cloudify.nodes.aws.efs.FileSystemTags',
    'cloudify.nodes.aws.kms.CustomerMasterKey',
    'cloudify.nodes.aws.kms.Alias',
    'cloudify.nodes.aws.kms.Grant',
    'cloudify.nodes.aws.CloudFormation.Stack',
    'cloudify.nodes.aws.ecs.Cluster',
    'cloudify.nodes.aws.ecs.Service',
    'cloudify.nodes.aws.ecs.TaskDefinition',
    'cloudify.nodes.swift.s3.Bucket',
    'cloudify.nodes.swift.s3.BucketObject',
    'cloudify.nodes.aws.eks.Cluster',
    'cloudify.nodes.aws.eks.NodeGroup',
    'cloudify.nodes.aws.codepipeline.Pipeline',
    'cloudify.nodes.resources.AmazonWebServices']

GCP_TYPES = [
    'cloudify.gcp.project',
    'cloudify.nodes.gcp.PolicyBinding',
    'cloudify.gcp.nodes.Instance',
    'cloudify.gcp.nodes.InstanceGroup',
    'cloudify.gcp.nodes.Volume',
    'cloudify.gcp.nodes.Snapshot',
    'cloudify.gcp.nodes.Network',
    'cloudify.gcp.nodes.SubNetwork',
    'cloudify.gcp.nodes.VPCNetworkPeering',
    'cloudify.gcp.nodes.Route',
    'cloudify.gcp.nodes.FirewallRule',
    'cloudify.gcp.nodes.SecurityGroup',
    'cloudify.gcp.nodes.Access',
    'cloudify.gcp.nodes.KeyPair',
    'cloudify.gcp.nodes.ExternalIP',
    'cloudify.gcp.nodes.GlobalAddress',
    'cloudify.gcp.nodes.StaticIP',
    'cloudify.gcp.nodes.Address',
    'cloudify.gcp.nodes.Image',
    'cloudify.gcp.nodes.HealthCheck',
    'cloudify.gcp.nodes.BackendService',
    'cloudify.gcp.nodes.RegionBackendService',
    'cloudify.gcp.nodes.UrlMap',
    'cloudify.gcp.nodes.TargetProxy',
    'cloudify.gcp.nodes.SslCertificate',
    'cloudify.gcp.nodes.ForwardingRule',
    'cloudify.gcp.nodes.GlobalForwardingRule',
    'cloudify.gcp.nodes.DNSZone',
    'cloudify.gcp.nodes.DNSRecord',
    'cloudify.gcp.nodes.DNSAAAARecord',
    'cloudify.gcp.nodes.DNSMXRecord',
    'cloudify.gcp.nodes.DNSNSRecord',
    'cloudify.gcp.nodes.DNSTXTRecord',
    'cloudify.gcp.nodes.KubernetesCluster',
    'cloudify.gcp.nodes.KubernetesNodePool',
    'cloudify.gcp.nodes.KubernetesClusterMonitoring',
    'cloudify.gcp.nodes.KubernetesClusterlegacyAbac',
    'cloudify.gcp.nodes.KubernetesClusterNetworkPolicy',
    'cloudify.gcp.nodes.Topic',
    'cloudify.gcp.nodes.TopicPolicy',
    'cloudify.gcp.nodes.TopicMessage',
    'cloudify.gcp.nodes.Subscription',
    'cloudify.gcp.nodes.SubscriptionPolicy',
    'cloudify.gcp.nodes.Acknowledge',
    'cloudify.gcp.nodes.PullRequest',
    'cloudify.gcp.nodes.StackDriverGroup',
    'cloudify.gcp.nodes.StackDriverTimeSeries',
    'cloudify.gcp.nodes.StackDriverUpTimeCheckConfig',
    'cloudify.gcp.nodes.LoggingSink',
    'cloudify.gcp.nodes.LoggingExclusion',
    'cloudify.gcp.nodes.Logging.BillingAccounts.sinks',
    'cloudify.gcp.nodes.Logging.Folders.sinks',
    'cloudify.gcp.nodes.Logging.Organizations.sinks',
    'cloudify.gcp.nodes.Logging.Projects.sinks',
    'cloudify.gcp.nodes.Logging.BillingAccounts.exclusions',
    'cloudify.gcp.nodes.Logging.Folders.exclusions',
    'cloudify.gcp.nodes.Logging.Organizations.exclusions',
    'cloudify.gcp.nodes.Logging.Organizatios.exclusions',
    'cloudify.gcp.nodes.Logging.Projects.exclusions',
    'cloudify.gcp.nodes.Logging.Projects.metrics',
    'cloudify.nodes.gcp.IAM.Role',
    'cloudify.nodes.gcp.Project',
    'cloudify.gcp.nodes.IAM.Role',
    'cloudify.nodes.gcp.Gcp'
]

AZURE_TYPES = [
    'cloudify.azure.nodes.ResourceGroup',
    'cloudify.azure.nodes.storage.StorageAccount'
    'cloudify.azure.nodes.storage.DataDisk'
    'cloudify.azure.nodes.storage.FileShare'
    'cloudify.azure.nodes.network.VirtualNetwork'
    'cloudify.azure.nodes.network.NetworkSecurityGroup'
    'cloudify.azure.nodes.network.NetworkSecurityRule'
    'cloudify.azure.nodes.network.Subnet'
    'cloudify.azure.nodes.network.RouteTable'
    'cloudify.azure.nodes.network.Route'
    'cloudify.azure.nodes.network.NetworkInterfaceCard'
    'cloudify.azure.nodes.network.IPConfiguration'
    'cloudify.azure.nodes.network.PublicIPAddress'
    'cloudify.azure.nodes.compute.AvailabilitySet'
    'cloudify.azure.nodes.compute.VirtualMachine'
    'cloudify.azure.nodes.compute.WindowsVirtualMachine'
    'cloudify.azure.nodes.compute.VirtualMachineExtension'
    'cloudify.azure.nodes.network.LoadBalancer'
    'cloudify.azure.nodes.network.LoadBalancer.BackendAddressPool'
    'cloudify.azure.nodes.network.LoadBalancer.Probe'
    'cloudify.azure.nodes.network.LoadBalancer.IncomingNATRule'
    'cloudify.azure.nodes.network.LoadBalancer.Rule'
    'cloudify.azure.Deployment'
    'cloudify.azure.nodes.compute.ContainerService'
    'cloudify.azure.nodes.Plan'
    'cloudify.azure.nodes.WebApp'
    'cloudify.azure.nodes.PublishingUser'
    'cloudify.azure.nodes.compute.ManagedCluster'
    'cloudify.nodes.azure.ResourceGroup'
    'cloudify.nodes.azure.storage.StorageAccount'
    'cloudify.nodes.azure.storage.DataDisk'
    'cloudify.nodes.azure.storage.FileShare'
    'cloudify.nodes.azure.network.VirtualNetwork'
    'cloudify.nodes.azure.network.NetworkSecurityGroup'
    'cloudify.nodes.azure.network.NetworkSecurityRule'
    'cloudify.nodes.azure.network.Subnet'
    'cloudify.nodes.azure.network.RouteTable'
    'cloudify.nodes.azure.network.Route'
    'cloudify.nodes.azure.network.NetworkInterfaceCard'
    'cloudify.nodes.azure.network.IPConfiguration'
    'cloudify.nodes.azure.network.PublicIPAddress'
    'cloudify.nodes.azure.compute.AvailabilitySet'
    'cloudify.nodes.azure.compute.VirtualMachine'
    'cloudify.nodes.azure.compute.WindowsVirtualMachine'
    'cloudify.nodes.azure.compute.VirtualMachineExtension'
    'cloudify.nodes.azure.network.LoadBalancer'
    'cloudify.nodes.azure.network.LoadBalancer.BackendAddressPool'
    'cloudify.nodes.azure.network.LoadBalancer.Probe'
    'cloudify.nodes.azure.network.LoadBalancer.IncomingNATRule'
    'cloudify.nodes.azure.network.LoadBalancer.Rule'
    'cloudify.nodes.azure.compute.ContainerService'
    'cloudify.nodes.azure.Plan'
    'cloudify.nodes.azure.WebApp'
    'cloudify.nodes.azure.PublishingUser'
    'cloudify.nodes.azure.compute.ManagedCluster'
    'cloudify.nodes.azure.resources.Azure'
    'cloudify.azure.nodes.resources.Azure'
    'cloudify.nodes.azure.CustomTypes'
]


REQUIRED_RELATIONSHIPS = {
    'cloudify.nodes.aws.ec2.Subnet': {
        'cloudify.nodes.aws.ec2.Vpc': 'cloudify.relationships.depends_on',
    },
    'cloudify.nodes.aws.ec2.SecurityGroup': {
        'cloudify.nodes.aws.ec2.Vpc': 'cloudify.relationships.depends_on',
    },
    'cloudify.nodes.aws.ec2.RouteTable': {
        'cloudify.nodes.aws.ec2.Vpc': 'cloudify.relationships.contained_in',
        'cloudify.nodes.aws.ec2.Subnet': 'cloudify.relationships.connected_to',
    },
    'cloudify.nodes.aws.ec2.Route': {
        'cloudify.nodes.aws.ec2.RouteTable':
            'cloudify.relationships.contained_in',
    },
    'cloudify.nodes.aws.ec2.SecurityGroupRuleIngress': {
        'cloudify.nodes.aws.ec2.SecurityGroup':
            'cloudify.relationships.contained_in',
    },
    'cloudify.nodes.aws.ec2.Interface': {
        'cloudify.nodes.aws.ec2.Subnet': 'cloudify.relationships.depends_on',
        'cloudify.nodes.aws.ec2.SecurityGroup':
            'cloudify.relationships.depends_on',
    },
    'cloudify.nodes.aws.ec2.Instances': {
        # 'cloudify.nodes.aws.ec2.Image':
        #     'cloudify.relationships.depends_on',
        'cloudify.nodes.aws.ec2.Interface':
            'cloudify.relationships.depends_on',
    },
    # azure
    'cloudify.nodes.azure.compute.VirtualMachine': {
        'cloudify.nodes.azure.ResourceGroup':
            'cloudify.relationships.azure.contained_in_resource_group',
        'cloudify.nodes.azure.storage.StorageAccount':
            'cloudify.relationships.azure.connected_to_storage_account',
        'cloudify.nodes.azure.network.NetworkInterfaceCard':
            'cloudify.relationships.azure.connected_to_nic',
    },
    'cloudify.nodes.azure.network.NetworkInterfaceCard': {
        'cloudify.nodes.azure.ResourceGroup':
            'cloudify.relationships.azure.contained_in_resource_group',
        'cloudify.nodes.azure.network.NetworkSecurityGroup':
            'cloudify.relationships.azure.'
            'nic_connected_to_network_security_group',
        'cloudify.nodes.azure.network.IPConfiguration':
            'cloudify.relationships.azure.nic_connected_to_ip_configuration'
    },
    'cloudify.nodes.azure.network.IPConfiguration': {
        'cloudify.nodes.azure.network.Subnet':
            'cloudify.relationships.azure.ip_configuration_connected_to_subnet', # noqa
    },
    'cloudify.nodes.azure.network.NetworkSecurityGroup': {
        'cloudify.nodes.azure.ResourceGroup':
            'cloudify.relationships.azure.contained_in_resource_group'
    },
    'cloudify.nodes.azure.network.PublicIPAddress': {
        'cloudify.nodes.azure.ResourceGroup':
            'cloudify.relationships.azure.contained_in_resource_group'
    },
    'cloudify.nodes.azure.network.Subnet': {
        'cloudify.nodes.azure.network.VirtualNetwork':
            'cloudify.relationships.azure.contained_in_virtual_network'
    },
    'cloudify.nodes.azure.network.VirtualNetwork': {
        'cloudify.nodes.azure.ResourceGroup':
            'cloudify.relationships.azure.contained_in_resource_group'
    },
    # gcp
    'cloudify.nodes.gcp.Instance': {
        'cloudify.nodes.gcp.FirewallRule':
            'cloudify.relationships.gcp.connected_to',
        'cloudify.nodes.gcp.SubNetwork':
            'cloudify.relationships.gcp.depends_on',
        'cloudify.nodes.gcp.Volume': 'cloudify.relationships.gcp.depends_on'
    },
    'cloudify.nodes.gcp.FirewallRule': {
        'cloudify.nodes.gcp.Network': 'cloudify.relationships.gcp.connected_to'
    },
    'cloudify.nodes.gcp.SubNetwork': {
        'cloudify.nodes.gcp.Network':
            'cloudify.relationships.gcp.contained_in_network'
    },
    # openstack
    'cloudify.nodes.openstack.Server': {
        'cloudify.nodes.openstack.Port':
            'cloudify.relationships.openstack.server_connected_to_port',
        'cloudify.nodes.CloudInit.CloudConfig':
            'cloudify.relationships.depends_on'
    },
    'cloudify.nodes.openstack.Subnet': {
        'cloudify.nodes.openstack.Network':
            'cloudify.relationships.contained_in',
        # 'cloudify.nodes.openstack.Router':
        #     'cloudify.relationships.openstack.subnet_connected_to_router'
    },
    'cloudify.nodes.openstack.FloatingIP': {
        'cloudify.nodes.openstack.Network':
            'cloudify.relationships.connected_to'
    },
    'cloudify.nodes.openstack.Port': {
        # 'cloudify.nodes.openstack.Subnet':
        #     'cloudify.relationships.openstack.port_connected_to_subnet',
        'cloudify.nodes.openstack.SecurityGroup':
            'cloudify.relationships.openstack.port_connected_to_security_group', # noqa
        # 'cloudify.nodes.openstack.FloatingIP':
        #     'cloudify.relationships.openstack.port_connected_to_floating_ip'
    },
    # terraform
    'cloudify.nodes.terraform.Module': {
        'cloudify.nodes.terraform':
            'cloudify.relationships.terraform.run_on_host',
    }
}

security_group_validation_aws = [
    'cloudify.nodes.aws.ec2.SecurityGroupRuleEgress',
    'cloudify.nodes.aws.ec2.SecurityGroupRuleIngress',
    'cloudify.nodes.aws.ec2.SecurityGroup'
]

security_group_validation_azure = [
    'cloudify.azure.nodes.network.NetworkSecurityGroup',
    'cloudify.azure.nodes.network.NetworkSecurityRule'
]

security_group_validation_openstack = [
    'cloudify.nodes.openstack.SecurityGroup'
]

AZURE_VALID_KEY = [
    'subscription_id',
    'tenant_id',
    'client_id',
    'client_secret']

AWS_VALID_KEY = [
    'aws_access_key_id',
    'aws_secret_access_key',
    'region_name',
    'aws_session_token']

firewall_rule_gcp = ['cloudify.gcp.nodes.FirewallRule']


TFLINT_SUPPORTED_CONFIGS = [
    'config',
    'plugin',
    'rule',
    'variables',
    'varfile',
    'ignore_module',
    'disabled_by_default',
    'force',
    'module',
    'plugin_dir'
]

TERRATAG_SUPPORTED_FLAGS = [
    'dir',
    'skipTerratagFiles',
    'verbose',
    'filter'
]

AWS_TYPE_WITH_TAGS = [
    # BaseType
    'cloudify.nodes.aws.ec2.Vpc',
    'cloudify.nodes.aws.ec2.VpcPeering',
    'cloudify.nodes.aws.ec2.Subnet',
    'cloudify.nodes.aws.ec2.SecurityGroup',
    'cloudify.nodes.aws.ec2.NATGateway',
    'cloudify.nodes.aws.ec2.Interface',
    'cloudify.nodes.aws.ec2.SpotFleetRequest',
    'cloudify.nodes.aws.ec2.Keypair',
    'cloudify.nodes.aws.ec2.NetworkACL',
    'cloudify.nodes.aws.ec2.VPNGateway',
    'cloudify.nodes.aws.ec2.CustomerGateway',
    'cloudify.nodes.aws.ec2.InternetGateway',
    'cloudify.nodes.aws.ec2.TransitGateway',
    'cloudify.nodes.aws.ec2.TransitGatewayRouteTable',
    'cloudify.nodes.aws.ec2.RouteTable',
    'cloudify.nodes.aws.ec2.EBSVolume',

    # tags_property
    'cloudify.nodes.aws.ec2.Instances',
    'cloudify.nodes.aws.ec2.SpotInstances',
    'cloudify.nodes.aws.ec2.ElasticIP',
]

DSL_1_3 = [
    'list',
    'dict',
    'regex',
    'float',
    'string',
    'integer',
    'boolean',
    'textarea'
]

DSL_1_4 = [
    'node_id',
    'node_ids',
    'blueprint_id',
    'node_template',
    'deployment_id',
    'blueprint_ids',
    'deployment_ids',
    'capability_value',
    'node_instance_ids',
]

DSL_1_5 = [
    'operation_name'
]

DSL_1_4.extend(DSL_1_3)
DSL_1_5.extend(DSL_1_4)

INPUTS_BY_DSL = {
    'cloudify_dsl_1_3': DSL_1_3,
    'cloudify_dsl_1_4': DSL_1_4,
    'cloudify_dsl_1_5': DSL_1_5
}

# SHOULD_BE_USER_PROVIDED
MASKED_ENV_VARS = [
    'AWS_SECRET_ACCESS_KEY',
    'AWS_ACCESS_KEY_ID',
    'ARM_CLIENT_ID',
    'ARM_CLIENT_SECRET'
]
