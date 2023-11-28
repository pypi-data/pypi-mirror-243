#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 
# @Author   : wgh


"""
文件说明：模型初始化
"""
import os
from FourthDimension.model.HuggingFaceBgeEmbeddings import HuggingFaceBgeEmbeddings

os.environ['HF_ENDPOINT'] = "https://hf-mirror.com"


def init_embeddings_model(model_name, model_kwargs, encode_kwargs):
    embeddings = HuggingFaceBgeEmbeddings(
        model_name=model_name,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs
    )
    return embeddings
