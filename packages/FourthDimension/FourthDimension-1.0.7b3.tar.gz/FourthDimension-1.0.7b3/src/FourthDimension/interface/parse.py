#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 
# @Author   : wgh


"""
文件说明：
"""
import os

from tqdm import tqdm

from FourthDimension.parser.docx_parser import parse_docx
from FourthDimension.parser.jsonl_parser import parse_jsonl


def parse_entrance(file_path, file_name):
    document = None
    if 'docx' in file_name:
        document = parse_docx(file_path, file_name)
    elif 'jsonl' in file_name:
        document = parse_jsonl(file_path, file_name)
    return document


def parse_data(doc_path):
    """
    数据解析
    :param doc_path: 文档路径
    :return:
    """
    print('开始文档解析...')
    all_contexts = get_all_docx_contexts(doc_path)
    return all_contexts


def get_file_paths_and_names(folder_path):
    if '.doc' in folder_path or '.docx' in folder_path or '.jsonl' in folder_path:
        return [(folder_path, os.path.basename(folder_path))]
    else:
        file_paths_and_names = []
        for root, dirs, files in os.walk(folder_path):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                file_paths_and_names.append((file_path, file_name))
    return file_paths_and_names


def get_all_docx_contexts(doc_path):
    all_contexts = []
    file_paths_and_names = get_file_paths_and_names(doc_path)
    if len(file_paths_and_names) < 10:
        for i, d in enumerate(file_paths_and_names):
            file_path = d[0]
            file_name = d[1]
            print('正在解析文档：' + file_name)
            document = parse_entrance(file_path, file_name)
            all_contexts.extend(document)
    else:
        print('正在解析文档...')
        for i, d in enumerate(tqdm(file_paths_and_names)):
            file_path = d[0]
            file_name = d[1]
            document = parse_entrance(file_path, file_name)
            all_contexts.extend(document)
    return all_contexts
