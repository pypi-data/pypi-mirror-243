#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 
# @Author   : wgh
import time

from FourthDimension.es.es_client import ElasticsearchClient
from FourthDimension.faiss_process.faiss_storage import embeddings_storage

es_client = ElasticsearchClient()


def upload_entrance(contexts):
    """
    存储入口
    :param contexts: 段落
    :return:
    """
    print('解析完成，文档上传中...')
    filter_context = es_upload(contexts)
    insert_file_name = faiss_upload(filter_context)
    print('已存储文档：{}'.format(insert_file_name))
    print('---------------------------------')


def es_upload(contexts):
    """
    es上传
    :param contexts: 段落
    :return:
    """
    filter_context = es_client.insert_data(contexts, 'chunk')
    return filter_context


def faiss_upload(contexts):
    """
    es上传
    :param contexts: 段落
    :return:
    """
    insert_file_name = embeddings_storage(contexts)
    return insert_file_name


def upload_test(contexts_path):
    pass
