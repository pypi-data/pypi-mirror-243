"""
Type annotations for textract service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_textract/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_textract.client import TextractClient

    session = Session()
    client: TextractClient = session.client("textract")
    ```
"""

import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from botocore.client import BaseClient, ClientMeta

from .literals import AutoUpdateType, FeatureTypeType
from .paginator import ListAdaptersPaginator, ListAdapterVersionsPaginator
from .type_defs import (
    AdaptersConfigTypeDef,
    AdapterVersionDatasetConfigTypeDef,
    AnalyzeDocumentResponseTypeDef,
    AnalyzeExpenseResponseTypeDef,
    AnalyzeIDResponseTypeDef,
    CreateAdapterResponseTypeDef,
    CreateAdapterVersionResponseTypeDef,
    DetectDocumentTextResponseTypeDef,
    DocumentLocationTypeDef,
    DocumentTypeDef,
    GetAdapterResponseTypeDef,
    GetAdapterVersionResponseTypeDef,
    GetDocumentAnalysisResponseTypeDef,
    GetDocumentTextDetectionResponseTypeDef,
    GetExpenseAnalysisResponseTypeDef,
    GetLendingAnalysisResponseTypeDef,
    GetLendingAnalysisSummaryResponseTypeDef,
    HumanLoopConfigTypeDef,
    ListAdaptersResponseTypeDef,
    ListAdapterVersionsResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    NotificationChannelTypeDef,
    OutputConfigTypeDef,
    QueriesConfigTypeDef,
    StartDocumentAnalysisResponseTypeDef,
    StartDocumentTextDetectionResponseTypeDef,
    StartExpenseAnalysisResponseTypeDef,
    StartLendingAnalysisResponseTypeDef,
    TimestampTypeDef,
    UpdateAdapterResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("TextractClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    BadDocumentException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    DocumentTooLargeException: Type[BotocoreClientError]
    HumanLoopQuotaExceededException: Type[BotocoreClientError]
    IdempotentParameterMismatchException: Type[BotocoreClientError]
    InternalServerError: Type[BotocoreClientError]
    InvalidJobIdException: Type[BotocoreClientError]
    InvalidKMSKeyException: Type[BotocoreClientError]
    InvalidParameterException: Type[BotocoreClientError]
    InvalidS3ObjectException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    ProvisionedThroughputExceededException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    UnsupportedDocumentException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class TextractClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/textract.html#Textract.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_textract/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        TextractClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/textract.html#Textract.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_textract/client/#exceptions)
        """

    def analyze_document(
        self,
        *,
        Document: DocumentTypeDef,
        FeatureTypes: Sequence[FeatureTypeType],
        HumanLoopConfig: HumanLoopConfigTypeDef = ...,
        QueriesConfig: QueriesConfigTypeDef = ...,
        AdaptersConfig: AdaptersConfigTypeDef = ...
    ) -> AnalyzeDocumentResponseTypeDef:
        """
        Analyzes an input document for relationships between detected items.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/textract.html#Textract.Client.analyze_document)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_textract/client/#analyze_document)
        """

    def analyze_expense(self, *, Document: DocumentTypeDef) -> AnalyzeExpenseResponseTypeDef:
        """
        `AnalyzeExpense` synchronously analyzes an input document for financially
        related relationships between
        text.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/textract.html#Textract.Client.analyze_expense)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_textract/client/#analyze_expense)
        """

    def analyze_id(self, *, DocumentPages: Sequence[DocumentTypeDef]) -> AnalyzeIDResponseTypeDef:
        """
        Analyzes identity documents for relevant information.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/textract.html#Textract.Client.analyze_id)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_textract/client/#analyze_id)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/textract.html#Textract.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_textract/client/#can_paginate)
        """

    def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/textract.html#Textract.Client.close)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_textract/client/#close)
        """

    def create_adapter(
        self,
        *,
        AdapterName: str,
        FeatureTypes: Sequence[FeatureTypeType],
        ClientRequestToken: str = ...,
        Description: str = ...,
        AutoUpdate: AutoUpdateType = ...,
        Tags: Mapping[str, str] = ...
    ) -> CreateAdapterResponseTypeDef:
        """
        Creates an adapter, which can be fine-tuned for enhanced performance on user
        provided
        documents.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/textract.html#Textract.Client.create_adapter)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_textract/client/#create_adapter)
        """

    def create_adapter_version(
        self,
        *,
        AdapterId: str,
        DatasetConfig: AdapterVersionDatasetConfigTypeDef,
        OutputConfig: OutputConfigTypeDef,
        ClientRequestToken: str = ...,
        KMSKeyId: str = ...,
        Tags: Mapping[str, str] = ...
    ) -> CreateAdapterVersionResponseTypeDef:
        """
        Creates a new version of an adapter.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/textract.html#Textract.Client.create_adapter_version)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_textract/client/#create_adapter_version)
        """

    def delete_adapter(self, *, AdapterId: str) -> Dict[str, Any]:
        """
        Deletes an Amazon Textract adapter.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/textract.html#Textract.Client.delete_adapter)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_textract/client/#delete_adapter)
        """

    def delete_adapter_version(self, *, AdapterId: str, AdapterVersion: str) -> Dict[str, Any]:
        """
        Deletes an Amazon Textract adapter version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/textract.html#Textract.Client.delete_adapter_version)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_textract/client/#delete_adapter_version)
        """

    def detect_document_text(
        self, *, Document: DocumentTypeDef
    ) -> DetectDocumentTextResponseTypeDef:
        """
        Detects text in the input document.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/textract.html#Textract.Client.detect_document_text)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_textract/client/#detect_document_text)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/textract.html#Textract.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_textract/client/#generate_presigned_url)
        """

    def get_adapter(self, *, AdapterId: str) -> GetAdapterResponseTypeDef:
        """
        Gets configuration information for an adapter specified by an AdapterId,
        returning information on AdapterName, Description, CreationTime, AutoUpdate
        status, and
        FeatureTypes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/textract.html#Textract.Client.get_adapter)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_textract/client/#get_adapter)
        """

    def get_adapter_version(
        self, *, AdapterId: str, AdapterVersion: str
    ) -> GetAdapterVersionResponseTypeDef:
        """
        Gets configuration information for the specified adapter version, including:
        AdapterId, AdapterVersion, FeatureTypes, Status, StatusMessage, DatasetConfig,
        KMSKeyId, OutputConfig, Tags and
        EvaluationMetrics.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/textract.html#Textract.Client.get_adapter_version)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_textract/client/#get_adapter_version)
        """

    def get_document_analysis(
        self, *, JobId: str, MaxResults: int = ..., NextToken: str = ...
    ) -> GetDocumentAnalysisResponseTypeDef:
        """
        Gets the results for an Amazon Textract asynchronous operation that analyzes
        text in a
        document.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/textract.html#Textract.Client.get_document_analysis)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_textract/client/#get_document_analysis)
        """

    def get_document_text_detection(
        self, *, JobId: str, MaxResults: int = ..., NextToken: str = ...
    ) -> GetDocumentTextDetectionResponseTypeDef:
        """
        Gets the results for an Amazon Textract asynchronous operation that detects
        text in a
        document.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/textract.html#Textract.Client.get_document_text_detection)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_textract/client/#get_document_text_detection)
        """

    def get_expense_analysis(
        self, *, JobId: str, MaxResults: int = ..., NextToken: str = ...
    ) -> GetExpenseAnalysisResponseTypeDef:
        """
        Gets the results for an Amazon Textract asynchronous operation that analyzes
        invoices and
        receipts.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/textract.html#Textract.Client.get_expense_analysis)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_textract/client/#get_expense_analysis)
        """

    def get_lending_analysis(
        self, *, JobId: str, MaxResults: int = ..., NextToken: str = ...
    ) -> GetLendingAnalysisResponseTypeDef:
        """
        Gets the results for an Amazon Textract asynchronous operation that analyzes
        text in a lending
        document.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/textract.html#Textract.Client.get_lending_analysis)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_textract/client/#get_lending_analysis)
        """

    def get_lending_analysis_summary(
        self, *, JobId: str
    ) -> GetLendingAnalysisSummaryResponseTypeDef:
        """
        Gets summarized results for the `StartLendingAnalysis` operation, which
        analyzes text in a lending
        document.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/textract.html#Textract.Client.get_lending_analysis_summary)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_textract/client/#get_lending_analysis_summary)
        """

    def list_adapter_versions(
        self,
        *,
        AdapterId: str = ...,
        AfterCreationTime: TimestampTypeDef = ...,
        BeforeCreationTime: TimestampTypeDef = ...,
        MaxResults: int = ...,
        NextToken: str = ...
    ) -> ListAdapterVersionsResponseTypeDef:
        """
        List all version of an adapter that meet the specified filtration criteria.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/textract.html#Textract.Client.list_adapter_versions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_textract/client/#list_adapter_versions)
        """

    def list_adapters(
        self,
        *,
        AfterCreationTime: TimestampTypeDef = ...,
        BeforeCreationTime: TimestampTypeDef = ...,
        MaxResults: int = ...,
        NextToken: str = ...
    ) -> ListAdaptersResponseTypeDef:
        """
        Lists all adapters that match the specified filtration criteria.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/textract.html#Textract.Client.list_adapters)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_textract/client/#list_adapters)
        """

    def list_tags_for_resource(self, *, ResourceARN: str) -> ListTagsForResourceResponseTypeDef:
        """
        Lists all tags for an Amazon Textract resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/textract.html#Textract.Client.list_tags_for_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_textract/client/#list_tags_for_resource)
        """

    def start_document_analysis(
        self,
        *,
        DocumentLocation: DocumentLocationTypeDef,
        FeatureTypes: Sequence[FeatureTypeType],
        ClientRequestToken: str = ...,
        JobTag: str = ...,
        NotificationChannel: NotificationChannelTypeDef = ...,
        OutputConfig: OutputConfigTypeDef = ...,
        KMSKeyId: str = ...,
        QueriesConfig: QueriesConfigTypeDef = ...,
        AdaptersConfig: AdaptersConfigTypeDef = ...
    ) -> StartDocumentAnalysisResponseTypeDef:
        """
        Starts the asynchronous analysis of an input document for relationships between
        detected items such as key-value pairs, tables, and selection
        elements.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/textract.html#Textract.Client.start_document_analysis)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_textract/client/#start_document_analysis)
        """

    def start_document_text_detection(
        self,
        *,
        DocumentLocation: DocumentLocationTypeDef,
        ClientRequestToken: str = ...,
        JobTag: str = ...,
        NotificationChannel: NotificationChannelTypeDef = ...,
        OutputConfig: OutputConfigTypeDef = ...,
        KMSKeyId: str = ...
    ) -> StartDocumentTextDetectionResponseTypeDef:
        """
        Starts the asynchronous detection of text in a document.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/textract.html#Textract.Client.start_document_text_detection)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_textract/client/#start_document_text_detection)
        """

    def start_expense_analysis(
        self,
        *,
        DocumentLocation: DocumentLocationTypeDef,
        ClientRequestToken: str = ...,
        JobTag: str = ...,
        NotificationChannel: NotificationChannelTypeDef = ...,
        OutputConfig: OutputConfigTypeDef = ...,
        KMSKeyId: str = ...
    ) -> StartExpenseAnalysisResponseTypeDef:
        """
        Starts the asynchronous analysis of invoices or receipts for data like contact
        information, items purchased, and vendor
        names.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/textract.html#Textract.Client.start_expense_analysis)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_textract/client/#start_expense_analysis)
        """

    def start_lending_analysis(
        self,
        *,
        DocumentLocation: DocumentLocationTypeDef,
        ClientRequestToken: str = ...,
        JobTag: str = ...,
        NotificationChannel: NotificationChannelTypeDef = ...,
        OutputConfig: OutputConfigTypeDef = ...,
        KMSKeyId: str = ...
    ) -> StartLendingAnalysisResponseTypeDef:
        """
        Starts the classification and analysis of an input document.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/textract.html#Textract.Client.start_lending_analysis)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_textract/client/#start_lending_analysis)
        """

    def tag_resource(self, *, ResourceARN: str, Tags: Mapping[str, str]) -> Dict[str, Any]:
        """
        Adds one or more tags to the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/textract.html#Textract.Client.tag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_textract/client/#tag_resource)
        """

    def untag_resource(self, *, ResourceARN: str, TagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Removes any tags with the specified keys from the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/textract.html#Textract.Client.untag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_textract/client/#untag_resource)
        """

    def update_adapter(
        self,
        *,
        AdapterId: str,
        Description: str = ...,
        AdapterName: str = ...,
        AutoUpdate: AutoUpdateType = ...
    ) -> UpdateAdapterResponseTypeDef:
        """
        Update the configuration for an adapter.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/textract.html#Textract.Client.update_adapter)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_textract/client/#update_adapter)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_adapter_versions"]
    ) -> ListAdapterVersionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/textract.html#Textract.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_textract/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_adapters"]) -> ListAdaptersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/textract.html#Textract.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_textract/client/#get_paginator)
        """
