#!/user/bin/env python3
# -*- coding: utf-8 -*-
"""
Copyright(C) 2023 baidu, Inc. All Rights Reserved

# @Time : 2023/9/5 17:02
# @Author : yangtingyu01
# @Email: yangtingyu01@baidu.com
# @File : blobstore.py
# @Software: PyCharm
"""
import boto3


class S3BlobStore:

    def __init__(self, bucket, endpoint_url, aws_access_key_id, aws_secret_access_key, region):
        """
        初始化s3对象
        :param bucket: s3的bucket名称
        :param endpoint_url: s3的endpoint地址
        :param aws_access_key_id: ak
        :param aws_secret_access_key: sk
        :param region: 地区
        """
        self._bucket = bucket
        self._client = boto3.client(
            "s3", aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key, endpoint_url=endpoint_url, region_name=region)

    def exist(self, path):
        """
        判断文件是否存在
        :param path: 文件路径
        :return:
        """
        try:
            self._client.head_object(Bucket=self._bucket, Key=path)
            return True
        except Exception as e:
            print(f"File {path} not exist: {e}")
            return False

    def read_file(self, path):
        """
        读取文件
        :param path: 文件路径
        :return:文件内容
        """
        response = self._client.get_object(Bucket=self._bucket, Key=path)
        data = response["Body"].read()
        return data

    def list_file(self, prefix=None):
        """
        列出文件
        :param prefix: 路径前缀
        :return: 文件名的列表
        """
        list_item = self._client.list_objects_v2(Bucket=self._bucket, Prefix=prefix)
        data_list = list_item.get("Contents", [])

        return data_list

    def write_file(self, dest_path, data):
        """
        写入文件
        :param dest_path: 路径
        :param data: 文件内容
        :return:
        """
        self._client.put_object(Body=data, Bucket=self._bucket, Key=dest_path)

    def upload_file(self, source_path, dest_path):
        """
        上传文件
        :param source_path: 本地路径
        :param dest_path: s3路径
        :return:
        """
        self._client.upload_file(source_path, self._bucket, dest_path)

    def copy(self, source_path, dest_path):
        """
        复制文件
        :param source_path: 源文件路径
        :param dest_path: 目标文件路径
        :return:
        """
        copy_source = {"Bucket": self._bucket, "Key": source_path}
        self._client.copy_object(
            CopySource=copy_source, Bucket=self._bucket, Key=dest_path)

    def download_file(self, source_path, dest_path):
        """
        下载文件
        :param source_path: 源文件路径
        :param dest_path: 目标文件路径
        """
        self._client.download_file(self._bucket, source_path, dest_path)

