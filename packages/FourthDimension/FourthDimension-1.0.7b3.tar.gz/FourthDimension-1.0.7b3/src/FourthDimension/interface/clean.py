#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 
# @Author   : wgh
from FourthDimension.es.es_client import ElasticsearchClient
from FourthDimension.faiss_process.faiss_storage import clean_faiss

es_client = ElasticsearchClient()


def clean_entrance():
    """
    清除数据入口
    """
    print('开始清除数据...')
    es_clean()
    print('数据清除中...')
    faiss_clean()
    print('数据已清除')
    print('---------------------------------')


def es_clean():
    """
    清除es中数据
    """
    es_client.clean_data()


def faiss_clean():
    """
    清空faiss数据
    :return:
    """
    clean_faiss()
