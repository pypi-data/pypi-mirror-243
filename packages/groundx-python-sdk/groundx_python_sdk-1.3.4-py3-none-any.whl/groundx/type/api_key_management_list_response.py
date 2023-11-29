# coding: utf-8

"""
    GroundX API

    Ground Your RAG Apps in Fact not Fiction

    The version of the OpenAPI document: 1.0.0
    Contact: support@groundx.ai
    Created by: https://www.groundx.ai/
"""

from datetime import datetime, date
import typing
from enum import Enum
from typing_extensions import TypedDict, Literal, TYPE_CHECKING

from groundx.type.api_key_management_list_response_api_keys import ApiKeyManagementListResponseApiKeys

class RequiredApiKeyManagementListResponse(TypedDict):
    pass

class OptionalApiKeyManagementListResponse(TypedDict, total=False):
    apiKeys: ApiKeyManagementListResponseApiKeys

class ApiKeyManagementListResponse(RequiredApiKeyManagementListResponse, OptionalApiKeyManagementListResponse):
    pass
