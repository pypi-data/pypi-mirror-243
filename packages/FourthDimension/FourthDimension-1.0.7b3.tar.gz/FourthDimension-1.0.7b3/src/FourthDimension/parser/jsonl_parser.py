#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 
# @Author   : wgh


"""
文件说明：
"""
import json

from FourthDimension.doc.document import Document
from FourthDimension.doc.spliter import RecursiveCharacterTextSplitter
from FourthDimension.config.config import config_setting

chunk_size = config_setting['para_config']['chunk_size']
chunk_overlap = config_setting['para_config']['overlap']

text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=chunk_size, chunk_overlap=chunk_overlap
)


def load_jsonl(file_path):
    data = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            data.append(json.loads(line))
    return data


def parse_jsonl(file_path, file_name):
    all_documents = []
    jsonl_data = load_jsonl(file_path)
    for i, line in enumerate(jsonl_data):
        document = Document(page_content=line['text'], metadata={'source': file_name})
        documents = text_splitter.split_documents([document])
        all_documents.extend(documents)
    return all_documents
