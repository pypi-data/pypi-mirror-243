#!/user/bin/env python3
# -*- coding: utf-8 -*-
"""
Copyright(C) 2023 baidu, Inc. All Rights Reserved

# @Time : 2023/8/8 15:30
# @Author : yangtingyu01
# @Email: yangtingyu01@baidu.com
# @File : artifact_client.py
# @Software: PyCharm
"""
from typing import List, Optional, Dict, Any
from baidubce.http import http_methods
from baidubce.http import handler
from baidubce import compat
from baidubce.auth import bce_v1_signer
from baidubce.http import bce_http_client
from baidubce.http import http_content_types
from baidubce.bce_base_client import BceBaseClient
from baidubce.auth.bce_credentials import BceCredentials
from baidubce.bce_client_configuration import BceClientConfiguration
from .paging import PagingRequest
import json


class ArtifactClient(BceBaseClient):
    """
    A client class for interacting with the Artifact service. Initializes with default configuration.

    This client provides an interface to interact with the Artifact service using BCE (Baidu Cloud Engine) API.
    It supports operations related to creating and retrieving artifacts within a specified workspace.

    Args:
        config (Optional[BceClientConfiguration]): The client configuration to use.
        ak (Optional[str]): Access key for authentication.
        sk (Optional[str]): Secret key for authentication.
        endpoint (Optional[str]): The service endpoint URL.
    """

    def __init__(self, config: Optional[BceClientConfiguration] = None, ak: Optional[str] = "",
                 sk: Optional[str] = "", endpoint: Optional[str] = ""):
        if config is None:
            config = BceClientConfiguration(credentials=BceCredentials(ak, sk), endpoint=endpoint)
        super(ArtifactClient, self).__init__(config=config)

    def _send_request(self, http_method, path, headers=None, params=None, body=None):
        """
        Send request to the Artifact service.
        """
        return bce_http_client.send_request(self.config, sign_wrapper([b'host', b'x-bce-date']),
                                            [handler.parse_json],
                                            http_method, path, body, headers, params)

    def create_artifact(self, uri: str, object_name: Optional[str] = "", alias: Optional[List] = None,
                        tags: Optional[Dict] = None, metadata: Optional[Any] = None,
                        description: Optional[str] = ""):
        """
        Create a new artifact.

        Args:
            uri (str): 版本文件路径, example:"s3://aiqa/store/workspaces/ws1/modelstores/ms1/models/model1/1"
            object_name (str): 数据完整名称, example:"workspaces/ws1/modelstores/ms1/models/model1"`
            alias (Optional[List]): 版本别名，如default, latest
            tags (Optional[Dict]): 版本标签
            metadata (Optional[Any]): 版本基本信息
            description (Optional[str]): 版本描述

        Returns:
            dict: The response containing information about the created artifact.
        """
        body = {"uri": uri,
                "alias": alias,
                "tags": tags,
                "metadata": metadata,
                "description": description,
                "objectName": object_name}
        return self._send_request(http_method=http_methods.POST,
                                  path=b"/v1/versions",
                                  params={"objectName": object_name},
                                  headers={b"Content-Type": http_content_types.JSON},
                                  body=json.dumps(body))

    def get_artifact(self, version: Optional[str] = "", object_name: Optional[str] = ""):
        """
        Get details of an artifact.

        Args:
            version (str): 版本, example:"1"
            object_name (str): 数据完整名称, example:"workspaces/ws1/modelstores/ms1/models/model1"`

        Returns:
            dict: The response containing details of the requested artifact.
        """
        return self._send_request(http_method=http_methods.GET,
                                  path=bytes("/v1/versions/"+version, encoding="utf-8"),
                                  params={"objectName": object_name})

    def list_artifact(self, object_name: Optional[str] = "", page_request: Optional[PagingRequest] = PagingRequest()):
        """
            List artifacts based on the specified parameters.

            Args:
                object_name (str): 数据完整名称，example:"workspaces/ws1/modelstores/ms1/models/model1"
                page_request (PagingRequest, optional): Paging request configuration. Default is PagingRequest().

            Returns:
                dict: Response from the service containing a list of artifacts.
        """
        params = {"objectName": object_name,
                  "pageNo": str(page_request.get_page_no()),
                  "pageSize": str(page_request.get_page_size()),
                  "order": page_request.order,
                  "orderBy": page_request.orderby}

        return self._send_request(http_method=http_methods.GET,
                                  path=bytes("/v1/versions", encoding="utf-8"),
                                  params=params)

    def update_artifact(self, object_name: Optional[str] = "", version: Optional[str] = "", alias: Optional[list] = "",
                        tags: Optional[dict] = None, description: Optional[str] = ""):
        """
        Update details of an artifact.

        Args:
            object_name (str): 数据完整名称, example:"workspaces/ws1/modelstores/ms1/models/model1"
            version (str): 版本 example:"1"
            alias (Optional[List]):  版本别名，如default, latest.
            tags (Optional[Dict]): 版本标签 [key:value]
            description (str): 版本描述, example:"artifact description"

        Returns:
            dict: The response containing information about the updated artifact.
        """
        body = {"alias": alias,
                "tags": tags,
                "description": description,
                "objectName": object_name,
                "version": version}
        return self._send_request(http_method=http_methods.PUT,
                                  path=bytes("/v1/versions/"+version, encoding="utf-8"),
                                  params={"objectName": object_name},
                                  headers={b"Content-Type": http_content_types.JSON},
                                  body=json.dumps(body))

    def delete_artifact(self, object_name: Optional[str] = "", version: Optional[str] = ""):
        """
        Delete an artifact.

        Args:
        object_name (str): 数据完整名称, example:"workspaces/ws1/modelstores/ms1/models/model1"
        version (str): 版本，如["1", "default"]

        Returns:
        dict: The response indicating the success of the deletion.
        """
        return self._send_request(http_method=http_methods.DELETE,
                                  path=bytes("/v1/versions/"+version, encoding="utf-8"),
                                  params={"objectName": object_name})

    def create_location(self, object_name: Optional[str] = "", style: Optional[str] = "Default"):
        """
        Create a new location.

        Args:
            object_name (str): 数据完整名称, example:"workspaces/ws1/modelstores/ms1/models/model1"
            style (str): 版本文件路径风格, binding:"omitempty,oneof=Default Triton" default:"Default""

        Returns:
            dict: The response containing information about the created location.
        """
        body = {"style": style, "objectName": object_name}
        return self._send_request(http_method=http_methods.POST,
                                  path=b"/v1/locations",
                                  params={"objectName": object_name},
                                  headers={b"Content-Type": http_content_types.JSON},
                                  body=json.dumps(body))


def sign_wrapper(headers_to_sign):
    """wrapper the bce_v1_signer.sign()."""
    def _wrapper(credentials, http_method, path, headers, params):
        credentials.access_key_id = compat.convert_to_bytes(credentials.access_key_id)
        credentials.secret_access_key = compat.convert_to_bytes(credentials.secret_access_key)

        return bce_v1_signer.sign(credentials,
                                  compat.convert_to_bytes(http_method),
                                  compat.convert_to_bytes(path), headers, params,
                                  headers_to_sign=headers_to_sign)
    return _wrapper