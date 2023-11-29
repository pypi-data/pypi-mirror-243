"""
Type annotations for kafka service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_kafka.client import KafkaClient

    session = Session()
    client: KafkaClient = session.client("kafka")
    ```
"""

import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from botocore.client import BaseClient, ClientMeta

from .literals import EnhancedMonitoringType, StorageModeType
from .paginator import (
    ListClientVpcConnectionsPaginator,
    ListClusterOperationsPaginator,
    ListClusterOperationsV2Paginator,
    ListClustersPaginator,
    ListClustersV2Paginator,
    ListConfigurationRevisionsPaginator,
    ListConfigurationsPaginator,
    ListKafkaVersionsPaginator,
    ListNodesPaginator,
    ListReplicatorsPaginator,
    ListScramSecretsPaginator,
    ListVpcConnectionsPaginator,
)
from .type_defs import (
    BatchAssociateScramSecretResponseTypeDef,
    BatchDisassociateScramSecretResponseTypeDef,
    BlobTypeDef,
    BrokerEBSVolumeInfoTypeDef,
    BrokerNodeGroupInfoTypeDef,
    ClientAuthenticationTypeDef,
    ConfigurationInfoTypeDef,
    ConnectivityInfoTypeDef,
    ConsumerGroupReplicationUpdateTypeDef,
    CreateClusterResponseTypeDef,
    CreateClusterV2ResponseTypeDef,
    CreateConfigurationResponseTypeDef,
    CreateReplicatorResponseTypeDef,
    CreateVpcConnectionResponseTypeDef,
    DeleteClusterResponseTypeDef,
    DeleteConfigurationResponseTypeDef,
    DeleteReplicatorResponseTypeDef,
    DeleteVpcConnectionResponseTypeDef,
    DescribeClusterOperationResponseTypeDef,
    DescribeClusterOperationV2ResponseTypeDef,
    DescribeClusterResponseTypeDef,
    DescribeClusterV2ResponseTypeDef,
    DescribeConfigurationResponseTypeDef,
    DescribeConfigurationRevisionResponseTypeDef,
    DescribeReplicatorResponseTypeDef,
    DescribeVpcConnectionResponseTypeDef,
    EmptyResponseMetadataTypeDef,
    EncryptionInfoTypeDef,
    GetBootstrapBrokersResponseTypeDef,
    GetClusterPolicyResponseTypeDef,
    GetCompatibleKafkaVersionsResponseTypeDef,
    KafkaClusterTypeDef,
    ListClientVpcConnectionsResponseTypeDef,
    ListClusterOperationsResponseTypeDef,
    ListClusterOperationsV2ResponseTypeDef,
    ListClustersResponseTypeDef,
    ListClustersV2ResponseTypeDef,
    ListConfigurationRevisionsResponseTypeDef,
    ListConfigurationsResponseTypeDef,
    ListKafkaVersionsResponseTypeDef,
    ListNodesResponseTypeDef,
    ListReplicatorsResponseTypeDef,
    ListScramSecretsResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListVpcConnectionsResponseTypeDef,
    LoggingInfoTypeDef,
    OpenMonitoringInfoTypeDef,
    ProvisionedRequestTypeDef,
    ProvisionedThroughputTypeDef,
    PutClusterPolicyResponseTypeDef,
    RebootBrokerResponseTypeDef,
    ReplicationInfoTypeDef,
    ServerlessRequestTypeDef,
    TopicReplicationUpdateTypeDef,
    UpdateBrokerCountResponseTypeDef,
    UpdateBrokerStorageResponseTypeDef,
    UpdateBrokerTypeResponseTypeDef,
    UpdateClusterConfigurationResponseTypeDef,
    UpdateClusterKafkaVersionResponseTypeDef,
    UpdateConfigurationResponseTypeDef,
    UpdateConnectivityResponseTypeDef,
    UpdateMonitoringResponseTypeDef,
    UpdateReplicationInfoResponseTypeDef,
    UpdateSecurityResponseTypeDef,
    UpdateStorageResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("KafkaClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    BadRequestException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    ForbiddenException: Type[BotocoreClientError]
    InternalServerErrorException: Type[BotocoreClientError]
    NotFoundException: Type[BotocoreClientError]
    ServiceUnavailableException: Type[BotocoreClientError]
    TooManyRequestsException: Type[BotocoreClientError]
    UnauthorizedException: Type[BotocoreClientError]


class KafkaClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka.html#Kafka.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        KafkaClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka.html#Kafka.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#exceptions)
        """

    def batch_associate_scram_secret(
        self, *, ClusterArn: str, SecretArnList: Sequence[str]
    ) -> BatchAssociateScramSecretResponseTypeDef:
        """
        Associates one or more Scram Secrets with an Amazon MSK cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka.html#Kafka.Client.batch_associate_scram_secret)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#batch_associate_scram_secret)
        """

    def batch_disassociate_scram_secret(
        self, *, ClusterArn: str, SecretArnList: Sequence[str]
    ) -> BatchDisassociateScramSecretResponseTypeDef:
        """
        Disassociates one or more Scram Secrets from an Amazon MSK cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka.html#Kafka.Client.batch_disassociate_scram_secret)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#batch_disassociate_scram_secret)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka.html#Kafka.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#can_paginate)
        """

    def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka.html#Kafka.Client.close)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#close)
        """

    def create_cluster(
        self,
        *,
        BrokerNodeGroupInfo: BrokerNodeGroupInfoTypeDef,
        ClusterName: str,
        KafkaVersion: str,
        NumberOfBrokerNodes: int,
        ClientAuthentication: ClientAuthenticationTypeDef = ...,
        ConfigurationInfo: ConfigurationInfoTypeDef = ...,
        EncryptionInfo: EncryptionInfoTypeDef = ...,
        EnhancedMonitoring: EnhancedMonitoringType = ...,
        OpenMonitoring: OpenMonitoringInfoTypeDef = ...,
        LoggingInfo: LoggingInfoTypeDef = ...,
        Tags: Mapping[str, str] = ...,
        StorageMode: StorageModeType = ...
    ) -> CreateClusterResponseTypeDef:
        """
        Creates a new MSK cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka.html#Kafka.Client.create_cluster)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#create_cluster)
        """

    def create_cluster_v2(
        self,
        *,
        ClusterName: str,
        Tags: Mapping[str, str] = ...,
        Provisioned: ProvisionedRequestTypeDef = ...,
        Serverless: ServerlessRequestTypeDef = ...
    ) -> CreateClusterV2ResponseTypeDef:
        """
        Creates a new MSK cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka.html#Kafka.Client.create_cluster_v2)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#create_cluster_v2)
        """

    def create_configuration(
        self,
        *,
        Name: str,
        ServerProperties: BlobTypeDef,
        Description: str = ...,
        KafkaVersions: Sequence[str] = ...
    ) -> CreateConfigurationResponseTypeDef:
        """
        Creates a new MSK configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka.html#Kafka.Client.create_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#create_configuration)
        """

    def create_replicator(
        self,
        *,
        KafkaClusters: Sequence[KafkaClusterTypeDef],
        ReplicationInfoList: Sequence[ReplicationInfoTypeDef],
        ReplicatorName: str,
        ServiceExecutionRoleArn: str,
        Description: str = ...,
        Tags: Mapping[str, str] = ...
    ) -> CreateReplicatorResponseTypeDef:
        """
        Creates the replicator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka.html#Kafka.Client.create_replicator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#create_replicator)
        """

    def create_vpc_connection(
        self,
        *,
        TargetClusterArn: str,
        Authentication: str,
        VpcId: str,
        ClientSubnets: Sequence[str],
        SecurityGroups: Sequence[str],
        Tags: Mapping[str, str] = ...
    ) -> CreateVpcConnectionResponseTypeDef:
        """
        Creates a new MSK VPC connection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka.html#Kafka.Client.create_vpc_connection)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#create_vpc_connection)
        """

    def delete_cluster(
        self, *, ClusterArn: str, CurrentVersion: str = ...
    ) -> DeleteClusterResponseTypeDef:
        """
        Deletes the MSK cluster specified by the Amazon Resource Name (ARN) in the
        request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka.html#Kafka.Client.delete_cluster)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#delete_cluster)
        """

    def delete_cluster_policy(self, *, ClusterArn: str) -> Dict[str, Any]:
        """
        Deletes the MSK cluster policy specified by the Amazon Resource Name (ARN) in
        the
        request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka.html#Kafka.Client.delete_cluster_policy)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#delete_cluster_policy)
        """

    def delete_configuration(self, *, Arn: str) -> DeleteConfigurationResponseTypeDef:
        """
        Deletes an MSK Configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka.html#Kafka.Client.delete_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#delete_configuration)
        """

    def delete_replicator(
        self, *, ReplicatorArn: str, CurrentVersion: str = ...
    ) -> DeleteReplicatorResponseTypeDef:
        """
        Deletes a replicator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka.html#Kafka.Client.delete_replicator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#delete_replicator)
        """

    def delete_vpc_connection(self, *, Arn: str) -> DeleteVpcConnectionResponseTypeDef:
        """
        Deletes a MSK VPC connection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka.html#Kafka.Client.delete_vpc_connection)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#delete_vpc_connection)
        """

    def describe_cluster(self, *, ClusterArn: str) -> DescribeClusterResponseTypeDef:
        """
        Returns a description of the MSK cluster whose Amazon Resource Name (ARN) is
        specified in the
        request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka.html#Kafka.Client.describe_cluster)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#describe_cluster)
        """

    def describe_cluster_operation(
        self, *, ClusterOperationArn: str
    ) -> DescribeClusterOperationResponseTypeDef:
        """
        Returns a description of the cluster operation specified by the ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka.html#Kafka.Client.describe_cluster_operation)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#describe_cluster_operation)
        """

    def describe_cluster_operation_v2(
        self, *, ClusterOperationArn: str
    ) -> DescribeClusterOperationV2ResponseTypeDef:
        """
        Returns a description of the cluster operation specified by the ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka.html#Kafka.Client.describe_cluster_operation_v2)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#describe_cluster_operation_v2)
        """

    def describe_cluster_v2(self, *, ClusterArn: str) -> DescribeClusterV2ResponseTypeDef:
        """
        Returns a description of the MSK cluster whose Amazon Resource Name (ARN) is
        specified in the
        request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka.html#Kafka.Client.describe_cluster_v2)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#describe_cluster_v2)
        """

    def describe_configuration(self, *, Arn: str) -> DescribeConfigurationResponseTypeDef:
        """
        Returns a description of this MSK configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka.html#Kafka.Client.describe_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#describe_configuration)
        """

    def describe_configuration_revision(
        self, *, Arn: str, Revision: int
    ) -> DescribeConfigurationRevisionResponseTypeDef:
        """
        Returns a description of this revision of the configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka.html#Kafka.Client.describe_configuration_revision)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#describe_configuration_revision)
        """

    def describe_replicator(self, *, ReplicatorArn: str) -> DescribeReplicatorResponseTypeDef:
        """
        Describes a replicator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka.html#Kafka.Client.describe_replicator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#describe_replicator)
        """

    def describe_vpc_connection(self, *, Arn: str) -> DescribeVpcConnectionResponseTypeDef:
        """
        Returns a description of this MSK VPC connection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka.html#Kafka.Client.describe_vpc_connection)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#describe_vpc_connection)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        Generate a presigned url given a client, its method, and arguments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka.html#Kafka.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#generate_presigned_url)
        """

    def get_bootstrap_brokers(self, *, ClusterArn: str) -> GetBootstrapBrokersResponseTypeDef:
        """
        A list of brokers that a client application can use to bootstrap.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka.html#Kafka.Client.get_bootstrap_brokers)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#get_bootstrap_brokers)
        """

    def get_cluster_policy(self, *, ClusterArn: str) -> GetClusterPolicyResponseTypeDef:
        """
        Get the MSK cluster policy specified by the Amazon Resource Name (ARN) in the
        request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka.html#Kafka.Client.get_cluster_policy)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#get_cluster_policy)
        """

    def get_compatible_kafka_versions(
        self, *, ClusterArn: str = ...
    ) -> GetCompatibleKafkaVersionsResponseTypeDef:
        """
        Gets the Apache Kafka versions to which you can update the MSK cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka.html#Kafka.Client.get_compatible_kafka_versions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#get_compatible_kafka_versions)
        """

    def list_client_vpc_connections(
        self, *, ClusterArn: str, MaxResults: int = ..., NextToken: str = ...
    ) -> ListClientVpcConnectionsResponseTypeDef:
        """
        Returns a list of all the VPC connections in this Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka.html#Kafka.Client.list_client_vpc_connections)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#list_client_vpc_connections)
        """

    def list_cluster_operations(
        self, *, ClusterArn: str, MaxResults: int = ..., NextToken: str = ...
    ) -> ListClusterOperationsResponseTypeDef:
        """
        Returns a list of all the operations that have been performed on the specified
        MSK
        cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka.html#Kafka.Client.list_cluster_operations)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#list_cluster_operations)
        """

    def list_cluster_operations_v2(
        self, *, ClusterArn: str, MaxResults: int = ..., NextToken: str = ...
    ) -> ListClusterOperationsV2ResponseTypeDef:
        """
        Returns a list of all the operations that have been performed on the specified
        MSK
        cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka.html#Kafka.Client.list_cluster_operations_v2)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#list_cluster_operations_v2)
        """

    def list_clusters(
        self, *, ClusterNameFilter: str = ..., MaxResults: int = ..., NextToken: str = ...
    ) -> ListClustersResponseTypeDef:
        """
        Returns a list of all the MSK clusters in the current Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka.html#Kafka.Client.list_clusters)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#list_clusters)
        """

    def list_clusters_v2(
        self,
        *,
        ClusterNameFilter: str = ...,
        ClusterTypeFilter: str = ...,
        MaxResults: int = ...,
        NextToken: str = ...
    ) -> ListClustersV2ResponseTypeDef:
        """
        Returns a list of all the MSK clusters in the current Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka.html#Kafka.Client.list_clusters_v2)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#list_clusters_v2)
        """

    def list_configuration_revisions(
        self, *, Arn: str, MaxResults: int = ..., NextToken: str = ...
    ) -> ListConfigurationRevisionsResponseTypeDef:
        """
        Returns a list of all the MSK configurations in this Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka.html#Kafka.Client.list_configuration_revisions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#list_configuration_revisions)
        """

    def list_configurations(
        self, *, MaxResults: int = ..., NextToken: str = ...
    ) -> ListConfigurationsResponseTypeDef:
        """
        Returns a list of all the MSK configurations in this Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka.html#Kafka.Client.list_configurations)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#list_configurations)
        """

    def list_kafka_versions(
        self, *, MaxResults: int = ..., NextToken: str = ...
    ) -> ListKafkaVersionsResponseTypeDef:
        """
        Returns a list of Apache Kafka versions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka.html#Kafka.Client.list_kafka_versions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#list_kafka_versions)
        """

    def list_nodes(
        self, *, ClusterArn: str, MaxResults: int = ..., NextToken: str = ...
    ) -> ListNodesResponseTypeDef:
        """
        Returns a list of the broker nodes in the cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka.html#Kafka.Client.list_nodes)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#list_nodes)
        """

    def list_replicators(
        self, *, MaxResults: int = ..., NextToken: str = ..., ReplicatorNameFilter: str = ...
    ) -> ListReplicatorsResponseTypeDef:
        """
        Lists the replicators.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka.html#Kafka.Client.list_replicators)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#list_replicators)
        """

    def list_scram_secrets(
        self, *, ClusterArn: str, MaxResults: int = ..., NextToken: str = ...
    ) -> ListScramSecretsResponseTypeDef:
        """
        Returns a list of the Scram Secrets associated with an Amazon MSK cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka.html#Kafka.Client.list_scram_secrets)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#list_scram_secrets)
        """

    def list_tags_for_resource(self, *, ResourceArn: str) -> ListTagsForResourceResponseTypeDef:
        """
        Returns a list of the tags associated with the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka.html#Kafka.Client.list_tags_for_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#list_tags_for_resource)
        """

    def list_vpc_connections(
        self, *, MaxResults: int = ..., NextToken: str = ...
    ) -> ListVpcConnectionsResponseTypeDef:
        """
        Returns a list of all the VPC connections in this Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka.html#Kafka.Client.list_vpc_connections)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#list_vpc_connections)
        """

    def put_cluster_policy(
        self, *, ClusterArn: str, Policy: str, CurrentVersion: str = ...
    ) -> PutClusterPolicyResponseTypeDef:
        """
        Creates or updates the MSK cluster policy specified by the cluster Amazon
        Resource Name (ARN) in the
        request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka.html#Kafka.Client.put_cluster_policy)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#put_cluster_policy)
        """

    def reboot_broker(
        self, *, BrokerIds: Sequence[str], ClusterArn: str
    ) -> RebootBrokerResponseTypeDef:
        """
        Reboots brokers.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka.html#Kafka.Client.reboot_broker)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#reboot_broker)
        """

    def reject_client_vpc_connection(
        self, *, ClusterArn: str, VpcConnectionArn: str
    ) -> Dict[str, Any]:
        """
        Returns empty response.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka.html#Kafka.Client.reject_client_vpc_connection)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#reject_client_vpc_connection)
        """

    def tag_resource(
        self, *, ResourceArn: str, Tags: Mapping[str, str]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Adds tags to the specified MSK resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka.html#Kafka.Client.tag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#tag_resource)
        """

    def untag_resource(
        self, *, ResourceArn: str, TagKeys: Sequence[str]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Removes the tags associated with the keys that are provided in the query.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka.html#Kafka.Client.untag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#untag_resource)
        """

    def update_broker_count(
        self, *, ClusterArn: str, CurrentVersion: str, TargetNumberOfBrokerNodes: int
    ) -> UpdateBrokerCountResponseTypeDef:
        """
        Updates the number of broker nodes in the cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka.html#Kafka.Client.update_broker_count)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#update_broker_count)
        """

    def update_broker_storage(
        self,
        *,
        ClusterArn: str,
        CurrentVersion: str,
        TargetBrokerEBSVolumeInfo: Sequence[BrokerEBSVolumeInfoTypeDef]
    ) -> UpdateBrokerStorageResponseTypeDef:
        """
        Updates the EBS storage associated with MSK brokers.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka.html#Kafka.Client.update_broker_storage)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#update_broker_storage)
        """

    def update_broker_type(
        self, *, ClusterArn: str, CurrentVersion: str, TargetInstanceType: str
    ) -> UpdateBrokerTypeResponseTypeDef:
        """
        Updates EC2 instance type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka.html#Kafka.Client.update_broker_type)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#update_broker_type)
        """

    def update_cluster_configuration(
        self, *, ClusterArn: str, ConfigurationInfo: ConfigurationInfoTypeDef, CurrentVersion: str
    ) -> UpdateClusterConfigurationResponseTypeDef:
        """
        Updates the cluster with the configuration that is specified in the request
        body.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka.html#Kafka.Client.update_cluster_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#update_cluster_configuration)
        """

    def update_cluster_kafka_version(
        self,
        *,
        ClusterArn: str,
        CurrentVersion: str,
        TargetKafkaVersion: str,
        ConfigurationInfo: ConfigurationInfoTypeDef = ...
    ) -> UpdateClusterKafkaVersionResponseTypeDef:
        """
        Updates the Apache Kafka version for the cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka.html#Kafka.Client.update_cluster_kafka_version)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#update_cluster_kafka_version)
        """

    def update_configuration(
        self, *, Arn: str, ServerProperties: BlobTypeDef, Description: str = ...
    ) -> UpdateConfigurationResponseTypeDef:
        """
        Updates an MSK configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka.html#Kafka.Client.update_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#update_configuration)
        """

    def update_connectivity(
        self, *, ClusterArn: str, ConnectivityInfo: ConnectivityInfoTypeDef, CurrentVersion: str
    ) -> UpdateConnectivityResponseTypeDef:
        """
        Updates the cluster's connectivity configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka.html#Kafka.Client.update_connectivity)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#update_connectivity)
        """

    def update_monitoring(
        self,
        *,
        ClusterArn: str,
        CurrentVersion: str,
        EnhancedMonitoring: EnhancedMonitoringType = ...,
        OpenMonitoring: OpenMonitoringInfoTypeDef = ...,
        LoggingInfo: LoggingInfoTypeDef = ...
    ) -> UpdateMonitoringResponseTypeDef:
        """
        Updates the monitoring settings for the cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka.html#Kafka.Client.update_monitoring)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#update_monitoring)
        """

    def update_replication_info(
        self,
        *,
        CurrentVersion: str,
        ReplicatorArn: str,
        SourceKafkaClusterArn: str,
        TargetKafkaClusterArn: str,
        ConsumerGroupReplication: ConsumerGroupReplicationUpdateTypeDef = ...,
        TopicReplication: TopicReplicationUpdateTypeDef = ...
    ) -> UpdateReplicationInfoResponseTypeDef:
        """
        Updates replication info of a replicator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka.html#Kafka.Client.update_replication_info)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#update_replication_info)
        """

    def update_security(
        self,
        *,
        ClusterArn: str,
        CurrentVersion: str,
        ClientAuthentication: ClientAuthenticationTypeDef = ...,
        EncryptionInfo: EncryptionInfoTypeDef = ...
    ) -> UpdateSecurityResponseTypeDef:
        """
        Updates the security settings for the cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka.html#Kafka.Client.update_security)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#update_security)
        """

    def update_storage(
        self,
        *,
        ClusterArn: str,
        CurrentVersion: str,
        ProvisionedThroughput: ProvisionedThroughputTypeDef = ...,
        StorageMode: StorageModeType = ...,
        VolumeSizeGB: int = ...
    ) -> UpdateStorageResponseTypeDef:
        """
        Updates cluster broker volume size (or) sets cluster storage mode to TIERED.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka.html#Kafka.Client.update_storage)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#update_storage)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_client_vpc_connections"]
    ) -> ListClientVpcConnectionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka.html#Kafka.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_cluster_operations"]
    ) -> ListClusterOperationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka.html#Kafka.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_cluster_operations_v2"]
    ) -> ListClusterOperationsV2Paginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka.html#Kafka.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_clusters"]) -> ListClustersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka.html#Kafka.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_clusters_v2"]) -> ListClustersV2Paginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka.html#Kafka.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_configuration_revisions"]
    ) -> ListConfigurationRevisionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka.html#Kafka.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_configurations"]
    ) -> ListConfigurationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka.html#Kafka.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_kafka_versions"]
    ) -> ListKafkaVersionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka.html#Kafka.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_nodes"]) -> ListNodesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka.html#Kafka.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_replicators"]
    ) -> ListReplicatorsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka.html#Kafka.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_scram_secrets"]
    ) -> ListScramSecretsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka.html#Kafka.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_vpc_connections"]
    ) -> ListVpcConnectionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka.html#Kafka.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kafka/client/#get_paginator)
        """
