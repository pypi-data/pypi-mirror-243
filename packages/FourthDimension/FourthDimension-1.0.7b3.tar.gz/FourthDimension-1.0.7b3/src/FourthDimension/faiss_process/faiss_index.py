#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 
# @Author   : wgh


"""
文件说明：
"""
import os

from FourthDimension.config.config import config_setting, embedding_model
from FourthDimension.faiss_process.FAISS import FAISS

top_k = config_setting['recall_config']['top_k']

# 获取当前脚本文件的路径
current_path = os.path.abspath(__file__)

# 获取当前脚本文件所在的目录
current_dir = os.path.dirname(current_path)

index_file = current_dir + '/../cache/faiss_cache'


def faiss_search(question):
    top_k_contexts = []
    db = FAISS.load_local(index_file, embedding_model)
    docs = db.similarity_search(question, k=top_k)
    for i, doc in enumerate(docs):
        top_k_contexts.append(doc.page_content)
    return top_k_contexts
