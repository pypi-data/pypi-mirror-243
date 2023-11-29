"""
Type annotations for marketplacecommerceanalytics service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_marketplacecommerceanalytics/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_marketplacecommerceanalytics.client import MarketplaceCommerceAnalyticsClient

    session = Session()
    client: MarketplaceCommerceAnalyticsClient = session.client("marketplacecommerceanalytics")
    ```
"""

from typing import Any, Dict, Mapping, Type

from botocore.client import BaseClient, ClientMeta

from .literals import DataSetTypeType, SupportDataSetTypeType
from .type_defs import (
    GenerateDataSetResultTypeDef,
    StartSupportDataExportResultTypeDef,
    TimestampTypeDef,
)

__all__ = ("MarketplaceCommerceAnalyticsClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    ClientError: Type[BotocoreClientError]
    MarketplaceCommerceAnalyticsException: Type[BotocoreClientError]

class MarketplaceCommerceAnalyticsClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplacecommerceanalytics.html#MarketplaceCommerceAnalytics.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_marketplacecommerceanalytics/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        MarketplaceCommerceAnalyticsClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplacecommerceanalytics.html#MarketplaceCommerceAnalytics.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_marketplacecommerceanalytics/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplacecommerceanalytics.html#MarketplaceCommerceAnalytics.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_marketplacecommerceanalytics/client/#can_paginate)
        """

    def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplacecommerceanalytics.html#MarketplaceCommerceAnalytics.Client.close)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_marketplacecommerceanalytics/client/#close)
        """

    def generate_data_set(
        self,
        *,
        dataSetType: DataSetTypeType,
        dataSetPublicationDate: TimestampTypeDef,
        roleNameArn: str,
        destinationS3BucketName: str,
        snsTopicArn: str,
        destinationS3Prefix: str = ...,
        customerDefinedValues: Mapping[str, str] = ...
    ) -> GenerateDataSetResultTypeDef:
        """
        Given a data set type and data set publication date, asynchronously publishes
        the requested data set to the specified S3 bucket and notifies the specified
        SNS topic once the data is
        available.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplacecommerceanalytics.html#MarketplaceCommerceAnalytics.Client.generate_data_set)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_marketplacecommerceanalytics/client/#generate_data_set)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplacecommerceanalytics.html#MarketplaceCommerceAnalytics.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_marketplacecommerceanalytics/client/#generate_presigned_url)
        """

    def start_support_data_export(
        self,
        *,
        dataSetType: SupportDataSetTypeType,
        fromDate: TimestampTypeDef,
        roleNameArn: str,
        destinationS3BucketName: str,
        snsTopicArn: str,
        destinationS3Prefix: str = ...,
        customerDefinedValues: Mapping[str, str] = ...
    ) -> StartSupportDataExportResultTypeDef:
        """
        *This target has been deprecated.* Given a data set type and a from date,
        asynchronously publishes the requested customer support data to the specified
        S3 bucket and notifies the specified SNS topic once the data is
        available.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplacecommerceanalytics.html#MarketplaceCommerceAnalytics.Client.start_support_data_export)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_marketplacecommerceanalytics/client/#start_support_data_export)
        """
