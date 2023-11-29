"""
Type annotations for kinesis-video-webrtc-storage service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesis_video_webrtc_storage/type_defs/)

Usage::

    ```python
    from mypy_boto3_kinesis_video_webrtc_storage.type_defs import ResponseMetadataTypeDef

    data: ResponseMetadataTypeDef = ...
    ```
"""

import sys
from typing import Dict

if sys.version_info >= (3, 12):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "ResponseMetadataTypeDef",
    "JoinStorageSessionInputRequestTypeDef",
    "EmptyResponseMetadataTypeDef",
)

ResponseMetadataTypeDef = TypedDict(
    "ResponseMetadataTypeDef",
    {
        "RequestId": str,
        "HostId": str,
        "HTTPStatusCode": int,
        "HTTPHeaders": Dict[str, str],
        "RetryAttempts": int,
    },
)
JoinStorageSessionInputRequestTypeDef = TypedDict(
    "JoinStorageSessionInputRequestTypeDef",
    {
        "channelArn": str,
    },
)
EmptyResponseMetadataTypeDef = TypedDict(
    "EmptyResponseMetadataTypeDef",
    {
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
