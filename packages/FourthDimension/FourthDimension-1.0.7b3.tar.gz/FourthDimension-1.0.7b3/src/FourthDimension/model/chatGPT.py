#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 
# @Author   : wgh
import openai

from FourthDimension.config.config import config_setting

answer_generation_model = config_setting['answer_generation_model']
openai.api_key = config_setting['openai']['api_key']
openai.api_base = config_setting['openai']['url']


def answer_generate(question, top_k_contexts):
    top_k_contexts_str = ""
    for i, d in enumerate(top_k_contexts):
        top_k_contexts_str += f"{i + 1}：{d}\n"
    prompt = "你的背景知识:{}；对话要求：1. 背景知识是最新的实时的信息，使用背景知识回答问题。" \
             "2. 优先使用背景知识的内容回答我的问题，答案应与背景知识严格一致。" \
             "3. 背景知识无法回答我的问题时，可以忽略背景知识，根据你的知识来自由回答。" \
             "4. 使用对话的风格，自然的回答问题。我的问题是:{}".format(top_k_contexts_str, question)
    # prompt = "{}以上是所有段落并以序号进行了标注，你现在作为基于以上所有段落的的阅读理解模型，请阅读以上所有段落并选择一个最合理的从中提取问题：{}" \
    #          "的答案并输出：<answer>，如果无答案则输出无答案".format(top_k_contexts_str, question)

    chat_completion = openai.ChatCompletion.create(
        model=answer_generation_model, messages=[{"role": "user", "content": prompt}]
    )
    answer = chat_completion.choices[0].message.content
    return answer
