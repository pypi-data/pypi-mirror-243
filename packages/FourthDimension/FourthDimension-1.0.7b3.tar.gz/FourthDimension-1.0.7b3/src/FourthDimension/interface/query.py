#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 
# @Author   : wgh
from FourthDimension.config.config import config_setting
from FourthDimension.es.es_client import ElasticsearchClient
from FourthDimension.faiss_process.faiss_index import faiss_search
from FourthDimension.utils.mix_sort import rerank

word_storage = config_setting['word_storage']
embedding_storage = config_setting['embedding_storage']
search_select = config_setting['search_select']
index_name = config_setting['elasticsearch_setting']['index_name']

elasticsearch = 'elasticsearch'
faiss = 'faiss'
elasticsearch_faiss = 'default'

es_client = ElasticsearchClient()


def query_entrance(question):
    """
    查询入口
    :param question: 问题
    :return:
    """
    print('开始检索问题：{}'.format(question))
    top_k_contexts = []
    if search_select == elasticsearch:
        top_k_contexts = es_query(question)
    elif search_select == faiss:
        top_k_contexts = faiss_query(question)
    elif search_select == elasticsearch_faiss:
        top_k_contexts = es_faiss_query(question)
    else:
        print(f"参数search_select无法匹配，请检查参数：f{search_select}")
    return top_k_contexts


def es_query(question):
    """
    es检索增强生成
    :param question: 问题
    :return:
    """
    top_k_contexts = es_client.es_search(question)
    return top_k_contexts


def faiss_query(question):
    """
    faiss检索
    :param question: 问题
    :return:
    """
    top_k_contexts = faiss_search(question)
    return top_k_contexts


def es_faiss_query(question):
    """
    es+faiss重排查询
    :param question: 问题
    :return:
    """
    es_top_k_contexts = es_query(question)
    faiss_top_k_contexts = faiss_query(question)
    merged_top_k = list(set(es_top_k_contexts + faiss_top_k_contexts))
    rerank_result = rerank(question, merged_top_k)
    return rerank_result
