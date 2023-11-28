#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 
# @Author   : wgh
from FourthDimension.document_loaders.json_loader import JSONLoader
from FourthDimension.interface.generate_answer import generate_answers
from FourthDimension.interface.upload import upload_entrance
from FourthDimension.interface.query import query_entrance
from FourthDimension.interface.clean import clean_entrance
from FourthDimension.interface.parse import parse_data


def upload_test(context_path):
    """
    测试上传接口
    :param context_path: context路径
    :return:
    """

    def metadata_func(record, metadata: dict) -> dict:
        metadata["id"] = record.get("id")
        return metadata

    loader = JSONLoader(
        file_path=context_path,
        jq_schema='.',
        content_key="text",
        json_lines=True,
        metadata_func=metadata_func
    )
    data = loader.load()
    print("数据load成功")
    upload_entrance(data)
    print("数据upload成功")


def recall_test(query):
    """
    文档上传接口
    :param query: 测试集问题
    :return:
    """
    return query_entrance(query)


def upload(doc_path):
    """
    文档上传接口
    数据格式List[Document]
    :param doc_path: 文档路径
    :return:
    """
    all_contexts = parse_data(doc_path)
    upload_entrance(all_contexts)


def query(question):
    """
    检索增强生成(问答)接口
    :param question: 问题
    :return:
    """
    top_k_contexts = query_entrance(question)
    answer = generate_answers(question, top_k_contexts)
    return answer


def clean():
    """
    清除所有数据
    """
    clean_entrance()
