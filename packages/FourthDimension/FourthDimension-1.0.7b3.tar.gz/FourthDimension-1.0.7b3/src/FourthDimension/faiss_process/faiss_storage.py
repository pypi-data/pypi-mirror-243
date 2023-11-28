#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 
# @Author   : wgh


"""
文件说明：
"""
import os
import shutil

from FourthDimension.config.config import embedding_model
from FourthDimension.faiss_process.FAISS import FAISS

# 获取当前脚本文件的路径
current_path = os.path.abspath(__file__)

# 获取当前脚本文件所在的目录
current_dir = os.path.dirname(current_path)

index_file = current_dir + '/../cache/faiss_cache'


def clean_faiss():
    if os.path.exists(index_file):
        shutil.rmtree(index_file)


def embeddings_storage(contexts):
    insert_data = []
    insert_file_name = []
    exist_file_name = []
    if os.path.exists(index_file):
        db = FAISS.load_local(index_file, embedding_model)
        db_data = db.docstore.__dict__
        for i, doc in enumerate(db_data['_dict'].items()):
            file_name = doc[1].metadata['source']
            exist_file_name.append(file_name)
        exist_file_name = list(set(exist_file_name))
        for i, doc in enumerate(contexts):
            file_name = doc.metadata['source']
            if file_name not in exist_file_name:
                insert_data.append(doc)
                insert_file_name.append(file_name)
        if len(insert_data) > 0:
            db.add_documents(insert_data)
            db.save_local(index_file)
    else:
        for i, doc in enumerate(contexts):
            file_name = doc.metadata['source']
            insert_file_name.append(file_name)
        db = FAISS.from_documents(contexts, embedding_model)
        db.save_local(index_file)
    insert_file_name = list(set(insert_file_name))
    return insert_file_name
