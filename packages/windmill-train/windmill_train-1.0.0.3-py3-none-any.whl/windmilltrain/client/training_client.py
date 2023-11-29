#!/user/bin/env python3
# -*- coding: utf-8 -*-
"""
Copyright(C) 2023 baidu, Inc. All Rights Reserved

# @Time : 2023/8/10 19:21
# @Author : yangtingyu01
# @Email: yangtingyu01@baidu.com
# @File : training_client.py
# @Software: PyCharm
"""
import json
from typing import Optional
from multidict import MultiDict
from baidubce.http import http_methods
from baidubce.http import bce_http_client
from baidubce.http import handler
from baidubce import compat
from baidubce.auth import bce_v1_signer
from baidubce.http import http_content_types
from baidubce.bce_base_client import BceBaseClient
from baidubce.auth.bce_credentials import BceCredentials
from baidubce.bce_client_configuration import BceClientConfiguration
from windmillartifactv1.client.artifact_api_artifact import ArtifactContent
from .paging import PagingRequest


class TrainingClient(BceBaseClient):
    """
    A client class for interacting with the Training service. Initializes with default configuration.

    This client provides an interface to send requests to the BceService for training-related operations.

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
        super(TrainingClient, self).__init__(config=config)

    def _send_request(self, http_method, path, headers=None, params=None, body=None):
        """
        Send request to BceService.
        """
        return bce_http_client.send_request(self.config, sign_wrapper([b'host', b'x-bce-date']),
                                            [handler.parse_json],
                                            http_method, path, body, headers, params)

    """
    job api
    """

    def create_job(self, workspace_id: str, project_name: str,
                   local_name: str, description: Optional[str] = "",
                   kind: Optional[str] = "Train", spec_kind: Optional[str] = "PaddleFlow",
                   spec_name: Optional[str] = "", experiment_name: Optional[str] = "",
                   create_if_not_exist: Optional[bool] = False, compute_name: Optional[str] = "",
                   filesystem_name: Optional[str] = "", resource_tips: Optional[list] = None,
                   parameters: Optional[dict] = None, config: Optional[dict] = None,
                   tags: Optional[dict] = None, datasets: Optional[list] = None):
        """
        Create a new training job.

        Args:
            workspace_id (str): 工作区id，example:"ws01"
            project_name (str): project localname. example:"project01"
            local_name (str): 任务名称 example:"job01"
            description (str): 任务描述 example:"job description"
            kind (str): 任务类型, default:"Train"
            spec_kind (str): spec 类型: Pod, PaddleFlow, Argo.
            spec_name (str): 部署作业的物料
            experiment_name (str): 实验名称
            create_if_not_exist (bool): 是否自动创建 experiment 实验
            compute_name (str):  计算资源名称
            filesystem_name (str): 文件系统资源名称
            resource_tips (list): 影响Suggest的过滤和排序的因素 比如 training
            parameters (dict): spec 文件参数, 如 pipeline 模板文件参数, {"train.flavour": "flavourgpu1"}
            config (dict): 配置文件参数
            tags (dict): 标签
            datasets (list): 训练用的数据集

        Returns:
            dict: The response from the server.
        """
        body = {"workspaceID": workspace_id,
                "projectName": project_name,
                "localName": local_name,
                "description": description,
                "kind": kind,
                "specKind": spec_kind,
                "specName": spec_name,
                "experimentName": experiment_name,
                "createIfNotExist": create_if_not_exist,
                "computeName": compute_name,
                "fileSystemName": filesystem_name,
                "tips": resource_tips,
                "parameters": parameters,
                "config": config,
                "tags": tags,
                "datasets": datasets}

        return self._send_request(http_method=http_methods.POST,
                                  path=bytes("/v1/workspaces/" + workspace_id +
                                             "/projects/" + project_name + "/jobs",
                                             encoding="utf-8"),
                                  headers={b"Content-Type": http_content_types.JSON},
                                  body=json.dumps(body))

    def list_job(self, workspace_id: str, project_name: str,
                 experiment_name: Optional[str] = "", status: Optional[str] = "",
                 filter_param: Optional[str] = "",
                 page_request: Optional[PagingRequest] = PagingRequest()):
        """
        List jobs based on specified criteria.

        Args:
            workspace_id (str): 工作区id
            project_name (str): project localName
            experiment_name (str): experiment localName
            status (str): job状态
            filter_param (str):the search keyword, search by localName, nameCN and description is supported.
            page_request (PagingRequest): Object containing paging request details.

        Returns:
            dict: The response from the server.
        """
        object_name = {"pageNo": str(page_request.get_page_no()),
                       "pageSize": str(page_request.get_page_size()),
                       "order": page_request.order,
                       "orderBy": page_request.orderby,
                       "filter": filter_param}

        return self._send_request(http_method=http_methods.GET,
                                  path=bytes("/v1/workspaces/" + workspace_id +
                                             "/projects/" + project_name + "/jobs",
                                             encoding="utf-8"),
                                  params=object_name)

    def get_job(self, workspace_id: str, project_name: str, local_name: str):
        """
        Get details of a specific job.

        Args:
            workspace_id (str): 工作区id
            project_name (str): project localname
            local_name (str): job名称

        Returns:
            dict: The response from the server.
        """
        return self._send_request(http_method=http_methods.GET,
                                  path=bytes("/v1/workspaces/" + workspace_id + "/projects/" +
                                             project_name + "/jobs/" + local_name, encoding="utf-8"))

    def update_job(self, workspace_id: str, project_name: str, local_name: str, description: Optional[str] = "",
                   tags: Optional[dict] = None):
        """
        Update the details of a specific job.

        Args:
            workspace_id (str): ID of the workspace containing the job.
            project_name (str): Name of the project containing the job.
            local_name (str): Local name of the job.
            description (str): New description for the job.
            tags (dict): New tags to associate with the job.

        Returns:
            dict: The response from the server.
        """
        body = {"workspaceID": workspace_id, "projectName": project_name,
                "localName": local_name, "description": description, "tags": tags}
        return self._send_request(http_method=http_methods.PUT,
                                  path=bytes("/v1/workspaces/" + workspace_id + "/projects/" +
                                             project_name + "/jobs/" + local_name, encoding="utf-8"),
                                  headers={b"Content-Type": http_content_types.JSON},
                                  body=json.dumps(body))

    def delete_job(self, workspace_id: str, project_name: str, local_name: str):
        """
        Delete a specific job.

        Args:
            workspace_id (str): 工作区id.
            project_name (str): project localname
            local_name (str): Local name of the job.

        Returns:
            dict: The response from the server.
        """
        return self._send_request(http_method=http_methods.DELETE,
                                  path=bytes("/v1/workspaces/" + workspace_id + "/projects/" +
                                             project_name + "/jobs/" + local_name, encoding="utf-8"))

    def stop_job(self, workspace_id: str, project_name: str, local_name: str):
        """
        Stop the execution of a specific job.

        Args:
            workspace_id (str): ID of the workspace containing the job.
            project_name (str): Name of the project containing the job.
            local_name (str): Local name of the job.

        Returns:
            dict: The response from the server.
        """
        return self._send_request(http_method=http_methods.POST,
                                  path=bytes("/v1/workspaces/" + workspace_id + "/projects/" +
                                             project_name + "/jobs/" + local_name + "/stop", encoding="utf-8"))

    """
    dataset api
    """

    def create_dataset(self, workspace_id: str, project_name: str, category: str, local_name: str,
                       artifact_uri: str, description: Optional[str] = "",
                       display_name: Optional[str] = "", data_type: Optional[str] = "",
                       annotation_type: Optional[str] = "", file_format: Optional[str] = "File",
                       annotation_format: Optional[str] = "Coco", artifact_description: Optional[str] = "",
                       artifact_alias: Optional[list] = None, artifact_tags: Optional[dict] = None,
                       artifact_metadata: Optional[dict] = None):
        """
        Create a new dataset

        Args:
            workspace_id (str): 工作区id
            project_name (str): project localname
            local_name (str): 数据集名称
            category (str): 数据集分类，用 "/" 表示级别
            description (str): 数据集描述
            display_name (str): 数据集中文名
            data_type (str): 数据集类型 image video
            annotation_type (str): Type of annotations.
            file_format (str): 数据集文件格式: Zip, File, Folder ...
            annotation_format (str): 数据集标注格式: Coco
            artifact_uri (str): 数据集版本文件路径. example:"s3://aiqa/store/workspaces/projects/default/datasets/default/versions/1"
            artifact_description (str): 数据集版本描述
            artifact_alias (list): 数据集版本别名，如default
            artifact_tags (dict): 数据集版本标签 [key:value]
            artifact_metadata (dict): 数据集版本基本信息

        Returns:
            dict: The response from the server.
        """
        artifact_content = {"uri": artifact_uri, "description": artifact_description, "alias": artifact_alias,
                            "tags": artifact_tags, "metadata": artifact_metadata}
        body = {"workspaceID": workspace_id, "projectName": project_name, "localName": local_name,
                "displayName": display_name, "description": description, "category": category,
                "fileFormat": file_format, "annotationFormat": annotation_format, "artifact": artifact_content}

        return self._send_request(http_method=http_methods.POST,
                                  path=bytes("/v1/workspaces/" + workspace_id +
                                             "/projects/" + project_name + "/datasets",
                                             encoding="utf-8"),
                                  headers={b"Content-Type": http_content_types.JSON},
                                  body=json.dumps(body))

    def list_dataset(self, workspace_id: str, project_name: str,
                     categories: Optional[list] = None, tags: Optional[dict] = None,
                     filter_param: Optional[str] = "",
                     page_request: Optional[PagingRequest] = PagingRequest()):
        """
        List the datasets

        Args:
            workspace_id (str): 工作区id
            project_name (str): project localname
            categories (list): 数据集分类，用 "/" 表示级别
            tags (dict): 数据集标签 [key:value]
            filter_param (str):the search keyword, search by localName, displayName and description is supported.
            page_request (PagingRequest): Parameters for the pagination request.
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
                object_name.add("categories", i)
        if tags:
            for i in tags:
                object_name.add("tags", i)
        return self._send_request(http_method=http_methods.GET,
                                  path=bytes("/v1/workspaces/" + workspace_id +
                                             "/projects/" + project_name + "/datasets",
                                             encoding="utf-8"),
                                  params=object_name)

    def get_dataset(self, workspace_id: str, project_name: str, local_name: str):
        """
        get the specific dataset by local name

        Args:
            workspace_id (str): 工作区id
            project_name (str): project local name
            local_name (str): 数据集名称
        Returns:
            dict: The response from the server.
        """
        return self._send_request(http_method=http_methods.GET,
                                  path=bytes("/v1/workspaces/" + workspace_id + "/projects/"
                                             + project_name + "/datasets/" + local_name, encoding="utf-8"))

    def update_dataset(self, workspace_id: str, project_name: str,
                       local_name: str, category: Optional[str],
                       display_name: Optional[str] = "", description: Optional[str] = "",
                       annotation_format: Optional[str] = "Coco"):
        """
        update a dataset by localname

        Args:
            workspace_id (str): 工作区id
            project_name (str): project local name
            local_name (str): 数据集名称
            category (str): 数据集分类
            display_name (str): 数据集中文名
            description (str): 数据集描述
            annotation_format (str): 数据集标注格式: Coco...
        Returns:
            dict: The response from the server.
        """
        body = {"displayName": display_name,
                "description": description,
                "category": category,
                "annotationFormat": annotation_format}
        return self._send_request(http_method=http_methods.PUT,
                                  path=bytes("/v1/workspaces/" + workspace_id + "/projects/"
                                             + project_name + "/datasets/" + local_name, encoding="utf-8"),
                                  headers={b"Content-Type": http_content_types.JSON},
                                  body=json.dumps(body))

    def delete_dataset(self, workspace_id: str, project_name: str, local_name: str):
        """
        delete a dataset by local name

        Args:
            workspace_id(str): 工作区id
            project_name(str): project local name
            local_name(str): 数据集名称
        Returns:
            dict: The response from the server.
        """
        return self._send_request(http_method=http_methods.DELETE,
                                  path=bytes("/v1/workspaces/" + workspace_id + "/projects/"
                                             + project_name + "/datasets/" + local_name, encoding="utf-8"))

    """
    pipeline api
    """
    def create_pipeline(self, workspace_id: str, project_name: str, local_name: str,
                        display_name: Optional[str] = "", description: Optional[str] = "",
                        category: Optional[str] = "", kind: Optional[str] = "",
                        artifact: Optional[ArtifactContent] = None):
        """
        create a pipeline by localname

        args：
            workspace_id (str): 工作区id
            project_name(str): project local name
            display_nam(str): pipeline 中文名
            local_name(str): pipeline名称
            description(str): pipeline描述
            category (str): pipeline分类
            kind(str): pipeline类型
            artifact(ArtifactContent): pipeline版本内容
        """
        body = {"workspaceID": workspace_id,
                "projectName": project_name,
                "localName": local_name,
                "displayName": display_name,
                "category": category,
                "description": description,
                "kind": kind,
                "artifact": {"uri": artifact.uri,
                             "description": artifact.description,
                             "alias": artifact.alias,
                             "tags": artifact.tags,
                             "metadata": artifact.metadata}}

        return self._send_request(http_method=http_methods.POST,
                                  path=bytes("/v1/workspaces/" + workspace_id +
                                             "/projects/" + project_name + "/pipelines",
                                             encoding="utf-8"),
                                  headers={b"Content-Type": http_content_types.JSON},
                                  body=json.dumps(body))

    def get_pipeline(self, workspace_id: str, project_name: str, local_name: str):
        """
        get the specific pipeline by local name

        Args:
            workspace_id(str): 工作区id
            project_name(str): project local name
            local_name(str): pipeline名称
        Returns:
            dict: The response from the server
        """
        return self._send_request(http_method=http_methods.GET,
                                  path=bytes("/v1/workspaces/" + workspace_id + "/projects/"
                                             + project_name + "/pipelines/" + local_name, encoding="utf-8"))

    def list_pipeline(self, workspace_id: str, project_name: str,
                      categories: Optional[list] = None, tags: Optional[dict] = None,
                      filter_param: Optional[str] = "",
                      page_request: Optional[PagingRequest] = PagingRequest()):
        """
        List the pipeline

        Args:
            workspace_id (str): 工作区id
            project_name (str): project localname
            categories (list): 产线分类，用 "/" 表示级别
            tags (dict):产线标签 [key:value]
            filter_param (str):the search keyword, search by localName, displayName and description is supported.
            page_request (PagingRequest): Parameters for the pagination request.
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
                object_name.add("categories", i)
        if tags:
            for i in tags:
                object_name.add("tags", i)
        return self._send_request(http_method=http_methods.GET,
                                  path=bytes("/v1/workspaces/" + workspace_id +
                                             "/projects/" + project_name + "/pipelines",
                                             encoding="utf-8"),
                                  params=object_name)
    """
    project_api
    """
    def list_project(self, workspace_id: str,
                     f: Optional[str] = "",
                     page_request: Optional[PagingRequest] = PagingRequest()):
        """
        List project by workspace_id

        args：
            workspace_id (str): 工作区id
            f:  filter
            page_request (PagingRequest): Parameters for the pagination request.
        """
        object_name = MultiDict()
        object_name.add("pageNo", str(page_request.get_page_no()))
        object_name.add("pageSize", str(page_request.get_page_size()))
        object_name.add("order", page_request.order)
        object_name.add("orderBy", page_request.orderby)
        object_name.add("filter", f)
        return self._send_request(http_method=http_methods.GET,
                                  path=bytes("/v1/workspaces/" + workspace_id +
                                             "/projects",
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