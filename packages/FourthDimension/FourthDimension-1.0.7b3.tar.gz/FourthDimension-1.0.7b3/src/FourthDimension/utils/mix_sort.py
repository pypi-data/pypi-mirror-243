#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 
# @Author   : wgh


"""
文件说明：
"""
from FourthDimension.utils.zutil import get_simi_score, chinese_segment
from FourthDimension.config.config import config_setting

top_k = config_setting['recall_config']['top_k']


def rerank(question, paras):
    para_scores = []
    for i, para in enumerate(paras):
        sents = chinese_segment(para)
        sents_score = []
        for context in sents:
            D = get_simi_score(question, context)
            sents_score.append({
                'sentence': context,
                'score': str(D[0][0])
            })
        result = [{k: float(v) if k == "score" else v for k, v in d.items()} for d in sents_score]
        sorted_dict_list = sorted(result, key=lambda x: x['score'])
        if len(sents) == 1:
            score = sum(d["score"] for d in sorted_dict_list) / len(sents)
        elif len(sents) == 2:
            score = sorted_dict_list[0]["score"] * 0.7 + sorted_dict_list[1]["score"]
        else:
            score = sorted_dict_list[0]["score"] * 0.5 + sorted_dict_list[1]["score"] * 0.3 + sorted_dict_list[2][
                "score"] * 0.2
        para_scores.append([i, score])
    sorted_para = sorted(para_scores, key=lambda x: x[1])
    paras_rerank_index = []
    for i in range(len(sorted_para)):
        paras_rerank_index.append(sorted_para[i][0])
    rerank_contexts = []
    for i, d in enumerate(paras_rerank_index):
        rerank_contexts.append(paras[d])
    return rerank_contexts
