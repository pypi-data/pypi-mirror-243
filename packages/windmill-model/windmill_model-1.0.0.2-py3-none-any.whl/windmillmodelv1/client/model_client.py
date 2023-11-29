#!/user/bin/env python3
# -*- coding: utf-8 -*-
"""
Copyright(C) 2023 baidu, Inc. All Rights Reserved

# @Time : 2023/8/21 15:58
# @Author : yangtingyu01
# @Email: yangtingyu01@baidu.com
# @File : model_client.py
# @Software: PyCharm
"""
import json
from multidict import MultiDict
from typing import Optional
from baidubce.http import http_methods
from baidubce.http import http_content_types
from baidubce.bce_base_client import BceBaseClient
from baidubce.auth.bce_credentials import BceCredentials
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.http import bce_http_client
from baidubce.http import handler
from baidubce import compat
from baidubce.auth import bce_v1_signer

from .paging import PagingRequest


class ModelClient(BceBaseClient):
    """
    A client class for interacting with the model service. Initializes with default configuration.

    This client provides an interface to interact with the model&model store service using BCE (Baidu Cloud Engine) API.
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
        super(ModelClient, self).__init__(config=config)

    def _send_request(self, http_method, path, headers=None, params=None, body=None):
        return bce_http_client.send_request(self.config, sign_wrapper([b'host', b'x-bce-date']),
                                            [handler.parse_json],
                                            http_method, path, body, headers, params)

    """
        model store api
        """

    def create_model_store(self, workspace_id: str, local_name: str, filesystem: str,
                           display_name: Optional[str] = "", description: Optional[str] = ""):
        """
        Creates a model store in the system.

        Args:
            workspace_id (str): 工作区 id
            local_name (str): 系统名称
            filesystem (str): 存储资源名称
            display_name (str, optional): 模型仓库名称
            description (str, optional): 模型仓库描述
        Returns:
            HTTP request response
        """
        body = {"workspaceID": workspace_id,
                "localName": local_name,
                "fileSystemName": filesystem,
                "displayName": display_name,
                "description": description
                }

        return self._send_request(http_method=http_methods.POST,
                                  headers={b"Content-Type": http_content_types.JSON},
                                  path=bytes("/v1/workspaces/" + workspace_id +
                                             "/modelstores",
                                             encoding="utf-8"),
                                  body=json.dumps(body))

    def list_model_store(self, workspace_id: str, filter_param: Optional[str] = "",
                         page_request: Optional[PagingRequest] = PagingRequest()):
        """
        Lists model stores in the system.
        Args:
            workspace_id (str): 工作区 id
            filter_param (str, optional): 搜索条件，支持系统名称、模型名称、描述。
            page_request (PagingRequest, optional): 分页请求配置。默认为 PagingRequest()。

        Returns:
            HTTP request response
        """
        params = {"filter": filter_param,
                  "pageNo": str(page_request.get_page_no()),
                  "pageSize": str(page_request.get_page_size()),
                  "order": page_request.order,
                  "orderBy": page_request.orderby}
        return self._send_request(http_method=http_methods.GET,
                                  path=bytes("/v1/workspaces/" + workspace_id +
                                             "/modelstores", encoding="utf-8"),
                                  params=params)

    def get_model_store(self, workspace_id: str, local_name: str):
        """
        Retrieves model store information.

        Args:
            workspace_id (str): 工作区 id
            local_name (str): 系统名称

        Returns:
            HTTP request response
        """
        return self._send_request(http_method=http_methods.GET,
                                  path=bytes("/v1/workspaces/" + workspace_id +
                                             "/modelstores/" + local_name, encoding="utf-8"))

    def update_model_store(self, workspace_id: str, local_name: str,
                           display_name: Optional[str] = "", description: Optional[str] = ""):
        """
        Updates model store information.

        Args:
            workspace_id (str): 工作区 id
            local_name (str): 系统名称
            display_name (str, optional): 模型仓库名称
            description (str, optional): 模型仓库描述

        Returns:
            HTTP request response
        """
        body = {"workspaceID": workspace_id,
                "modelStoreName": local_name,
                "displayName": display_name,
                "description": description
                }

        return self._send_request(http_method=http_methods.PUT,
                                  path=bytes("/v1/workspaces/" + workspace_id +
                                             "/modelstores/" + local_name,
                                             encoding="utf-8"),
                                  body=json.dumps(body))

    def delete_model_store(self, workspace_id: str, local_name: str):
        """
        Deletes a model store from the system.

        Args:
            workspace_id (str): 工作区 id
            local_name (str): 系统名称

        Returns:
            HTTP request response
        """
        return self._send_request(http_method=http_methods.DELETE,
                                  path=bytes("/v1/workspaces/" + workspace_id +
                                             "/modelstores/" + local_name, encoding="utf-8"))

    """
    model api
    """

    def create_model(self, workspace_id: str, model_store_name: str,
                     local_name: str, category: str, model_formats: list,
                     display_name: Optional[str] = "", description: Optional[str] = "",
                     schema_uri: Optional[str] = "", artifact_uri: Optional[str] = "",
                     artifact_description: Optional[str] = "", artifact_alias: Optional[list] = None,
                     artifact_metadata: Optional[str] = "", artifact_tags: Optional[dict] = None):
        """
        创建模型。

        Args:
            workspace_id (str): 工作区 id，例如："ws01"。
            model_store_name (str): 模型仓库名称，例如："ms01"。
            local_name (str): 系统名称，例如："model01"。
            category (str): 模型类别，例如："Image/OCR"。
            model_formats (list): 模型文件框架类型，例如：["PaddlePaddle"]。
            display_name (str, optional): 模型名称，例如："模型01"。
            description (str, optional): 模型描述，例如："模型描述"。
            schema_uri (str, optional): 模型对应的预测服务的接口文档地址。
            artifact_uri (str, optional): 版本文件路径。
            artifact_description (str, optional): 版本描述。
            artifact_alias (list, optional): 版本别名，例如 ["default"]。
            artifact_metadata (str, optional): 版本基本信息。
            artifact_tags (dict, optional): 版本标签。

        Returns:
            HTTP request response
        """
        body = {"workspaceID": workspace_id,
                "modelStoreName": model_store_name,
                "localName": local_name,
                "displayName": display_name,
                "description": description,
                "category": category,
                "modelFormats": model_formats,
                "schemaUri": schema_uri,
                "artifact": {
                    "uri": artifact_uri,
                    "description": artifact_description,
                    "alias": artifact_alias,
                    "tags": artifact_tags,
                    "metadata": artifact_metadata
                }
        }
        return self._send_request(http_method=http_methods.POST,
                                  headers={b"Content-Type": http_content_types.JSON},
                                  path=bytes("/v1/workspaces/" + workspace_id +
                                             "/modelstores/" + model_store_name + "/models", encoding="utf-8"),
                                  body=json.dumps(body))

    def list_model(self, workspace_id: str, model_store_name: str,
                   category: Optional[str] = "", tags: Optional[str] = "",
                   filter_param: Optional[str] = "", page_request: Optional[PagingRequest] = PagingRequest()):
        """

        Lists models in the system.

        Args:
            workspace_id (str): 工作区 id
            model_store_name (str): 模型仓库名称
            category (str, optional): 按模型类别筛选模型
            tags (str, optional): 按模型版本标签筛选模型
            filter_param (str, optional): 搜索条件，支持系统名称、模型名称、描述。
            page_request (PagingRequest, optional): 分页请求配置。默认为 PagingRequest()。
        Returns:
            HTTP request response
        """
        params = MultiDict()
        params.add("pageNo", str(page_request.get_page_no()))
        params.add("pageSize", str(page_request.get_page_size()))
        params.add("order", page_request.order)
        params.add("orderBy", page_request.orderby)
        params.add("filter", filter_param)
        if category:
            for i in category:
                params.add("categories", i)
        if tags:
            for i in tags:
                params.add("tags", i)
        return self._send_request(http_method=http_methods.GET,
                                  path=bytes("/v1/workspaces/" + workspace_id +
                                             "/modelstores/" + model_store_name + "/models", encoding="utf-8"),
                                  params=params)

    def get_model(self, workspace_id: str, model_store_name: str, local_name: str):
        """
        Retrieves model information.

            Args:
                local_name (str): 系统名称，例如："model01"
                model_store_name (str): 模型仓库名称，例如："ms01"
                workspace_id (str): 工作区 id，例如："ws01"
         Returns:
            HTTP request response
        """
        return self._send_request(http_method=http_methods.GET,
                                  path=bytes("/v1/workspaces/" + workspace_id +
                                             "/modelstores/" + model_store_name + "/models/" + local_name,
                                             encoding="utf-8"))

    def update_model(self, workspace_id: str, model_store_name: str, local_name: str,
                     category: str, display_name: Optional[str] = "", description: Optional[str] = "",
                     model_formats: Optional[str] = "", schema_uri: Optional[str] = ""):
        """
        Updates model information.

        Args:
            workspace_id (str): 工作区 id
            model_store_name (str): 模型仓库名称
            local_name (str): 系统名称
            display_name (str, optional): 模型名称，例如："模型01"
            description (str, optional): 模型描述，例如："model description"
            category (str, optional): 模型类别，例如："Image/OCR"
            model_formats (str, optional): 模型文件框架类型，例如："[PaddlePaddle]"
            schema_uri (str, optional): 模型对应的预测服务的接口文档地址

        Returns:
            HTTP request response
        """
        body = {
            key: value
            for key, value in {
                "displayName": display_name,
                "description": description,
                "category": category,
                "modelFormats": model_formats,
                "workspaceID": workspace_id,
                "modelStoreName": model_store_name,
                "localName": local_name,
                "schemaUri": schema_uri
            }.items()
            if value != ""
        }

        return self._send_request(http_method=http_methods.PUT,
                                  headers={b"Content-Type": http_content_types.JSON},
                                  path=bytes("/v1/workspaces/" + workspace_id +
                                             "/modelstores/" + model_store_name + "/models/" + local_name,
                                             encoding="utf-8"),
                                  body=json.dumps(body))

    def delete_model(self, workspace_id: str, model_store_name: str, local_name: str):
        """
        Deletes a model from the system.

        Args:
            workspace_id (str): 工作区 id
            model_store_name (str): 模型仓库名称
            local_name (str): 系统名称
        Returns:
            HTTP request response
        """
        return self._send_request(http_method=http_methods.DELETE,
                                  path=bytes("/v1/workspaces/" + workspace_id +
                                             "/modelstores/" + model_store_name + "/models/" + local_name,
                                             encoding="utf-8"))


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

