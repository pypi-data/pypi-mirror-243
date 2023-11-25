# !/user/bin/env python3
# -*- coding: utf-8 -*-
"""
Copyright(C) 2023 baidu, Inc. All Rights Reserved

# @Time : 2023/11/25 13:41
# @Author : yangtingyu01
# @Email: yangtingyu01@baidu.com
# @File : annotation_client.py
# @Software: PyCharm
"""
from typing import Optional
from multidict import MultiDict
from baidubce.http import http_methods
from baidubce.http import bce_http_client
from baidubce.http import handler
from baidubce import compat
from baidubce.auth import bce_v1_signer
from baidubce.bce_base_client import BceBaseClient
from baidubce.auth.bce_credentials import BceCredentials
from baidubce.bce_client_configuration import BceClientConfiguration

from sdk.python.paging import PagingRequest


class AnnotationClient(BceBaseClient):
    """
    A client class for interacting with the Annotation service. Initializes with default configuration.

    This client provides an interface to send requests to the BceService.

    Args:
            config (Optional[BceClientConfiguration]): The client configuration to use.
            ak (Optional[str]): Access key for authentication.
            sk (Optional[str]): Secret key for authentication.
            endpoint (Optional[str]): The service endpoint URL.
    """

    def __init__(self, config: Optional[BceClientConfiguration] = None, ak: Optional[str] = "",
                 sk: Optional[str] = "", endpoint: Optional[str] = ""):
        """
        Initialize the TrainingClient with the provided configuration.
        """
        if config is None:
            config = BceClientConfiguration(credentials=BceCredentials(ak, sk), endpoint=endpoint)
        super(AnnotationClient, self).__init__(config=config)

    def _send_request(self, http_method, path, headers=None, params=None, body=None):
        """
        Send request to BceService.
        """
        return bce_http_client.send_request(self.config, sign_wrapper([b'host', b'x-bce-date']),
                                            [handler.parse_json],
                                            http_method, path, body, headers, params)

    def list_annotation_set(self, workspace_id: str, project_name: str,
                            categories: Optional[str] = "",
                            filter_param: Optional[str] = "",
                            page_request: Optional[PagingRequest] = PagingRequest()):
        """
                List jobs based on specified criteria.

                Args:
                    workspace_id (str): 工作区id
                    project_name (str): project localName
                    categories (str): 按分类筛选  example: categories=Image/OCR&categories=Image/AnomalyDetection
                    filter_param (str):Filter the search keyword, search by localName, displayName and
                    description is supported.
                    page_request (PagingRequest): Object containing paging request details.

                Returns:
                    dict: The response from the server.
                """
        object_name = MultiDict()
        object_name.add("pageNo", str(page_request.get_page_no()))
        object_name.add("pageSize", str(page_request.get_page_size()))
        object_name.add("order", page_request.order)
        object_name.add("orderBy", page_request.orderby)
        object_name.add("filter", filter_param)
        if categories:
            for i in categories:
                object_name.add("category", i)

        return self._send_request(http_method=http_methods.GET,
                                  path=bytes("/v1/workspaces/" + workspace_id +
                                             "/projects/" + project_name + "/annotationsets",
                                             encoding="utf-8"),
                                  params=object_name)


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
