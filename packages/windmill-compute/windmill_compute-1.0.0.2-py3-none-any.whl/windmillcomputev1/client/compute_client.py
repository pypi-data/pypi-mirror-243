#!/user/bin/env python3
# -*- coding: utf-8 -*-
"""
Copyright(C) 2023 baidu, Inc. All Rights Reserved

# @Time : 2023/8/25 15:45
# @Author : yangtingyu01
# @Email: yangtingyu01@baidu.com
# @File : compute_client.py
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
import json
from .paging import PagingRequest


class ComputeClient(BceBaseClient):
    """
    A client class for interacting with the compute service. Initializes with default configuration.

    This client provides an interface to interact with the compute service using BCE (Baidu Cloud Engine) API.
    It supports operations related to creating and retrieving compute within a specified workspace.
    """

    def __init__(self, config: Optional[BceClientConfiguration] = None, ak: Optional[str] = "",
                 sk: Optional[str] = "", endpoint: Optional[str] = ""):
        """
        构造函数：用于初始化 ComputeClient 对象。

        Args:
            config (Optional[BceClientConfiguration], optional): 一个包含配置信息的对象，默认为 None。
            ak (Optional[str], optional): 用户的 AK（Access Key），默认为空字符串。
            sk (Optional[str], optional): 用户的 SK（Secret Key），默认为空字符串。
            endpoint (Optional[str], optional): 请求的终端点地址，默认为空字符串。

        Returns:
            None

        """
        if config is None:
            config = BceClientConfiguration(credentials=BceCredentials(ak, sk), endpoint=endpoint)
        super(ComputeClient, self).__init__(config=config)

    def _send_request(self, http_method, path, headers=None, params=None, body=None):
        """
        Send request to the Artifact service.
        """
        return bce_http_client.send_request(self.config, sign_wrapper([b'host', b'x-bce-date']),
                                            [handler.parse_json],
                                            http_method, path, body, headers, params)

    def get_filesystem(self, workspace_id: str, local_name: str):
        """
        Gets a filesystem object from specified workspace.
        :param workspace_id: 工作区id
        :param local_name: filesystem name
        :return:
        """
        return self._send_request(http_method=http_methods.GET,
                                  path=bytes("/v1/workspaces/" + workspace_id + "/filesystems/" + local_name,
                                             encoding="utf-8"))

    """
       compute api
       """

    def get_compute(self, workspace_id: str, local_name: str):
        """
        Gets compute object from specified workspace.
        :param workspace_id:
        :param local_name:
        :return:
        """
        return self._send_request(http_method=http_methods.GET,
                                  path=bytes("/v1/workspaces/" + workspace_id + "/computes/" + local_name,
                                             encoding="utf-8"))

    def list_compute(self, workspace_id: str, parent_name: Optional[str] = "", kind: Optional[str] = "",
                     host: Optional[str] = "", namespace: Optional[str] = "",
                     filter_param: Optional[str] = "",
                     page_request: Optional[PagingRequest] = PagingRequest()):
        """
        Lists model stores in the system.
        Args:
            workspace_id (str): 工作区 id
            filter_param (str, optional): 搜索条件，支持系统名称、模型名称、描述。
            page_request (PagingRequest, optional): 分页请求配置。默认为 PagingRequest()。
            parent_name (str, optional):
            kind (str, optional):
            host (str, optional):
            namespace (str, optional):

        Returns:
            HTTP request response
        """
        params = {
                  "filter": filter_param,
                  "parentName": parent_name,
                  "kind": kind,
                  "namespace": namespace,
                  "host": host,
                  "pageNo": str(page_request.get_page_no()),
                  "pageSize": str(page_request.get_page_size()),
                  "order": page_request.order,
                  "orderBy": page_request.orderby}
        return self._send_request(http_method=http_methods.GET,
                                  path=bytes("/v1/workspaces/" + workspace_id + "/computes", encoding="utf-8"),
                                  params=params)


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
