#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 
# @Author   : wgh


"""
文件说明：
"""
from FourthDimension.model.chatGPT import answer_generate


def generate_answers(question, data):
    """
    答案生成
    :param question: 问题
    :param data: 召回结果
    :return:
    """
    if len(data) > 0:
        print('检索已召回，答案生成中...')
        answer = answer_generate(question, data)
        print('答案：{}'.format(answer))
        print('---------------------------------')
        return answer
    else:
        print('无检索结果，请确认是否上传文档')
