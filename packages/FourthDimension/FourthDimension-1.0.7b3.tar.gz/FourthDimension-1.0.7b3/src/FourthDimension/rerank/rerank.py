#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 
# @Author   : wgh
import re

import jieba
from fuzzywuzzy import fuzz

from FourthDimension.config.config import patterns, patternsLen


class DocQAAnswerEntity:
    def init(self, content, question, fuzz_score, words_ratio):
        self.content = content
        self.question = question
        self.fuzz_score = fuzz_score
        self.words_ratio = words_ratio


def getDetailResult(datas, question, question_anal):
    question_analysisCut = jieba.lcut(question_anal)
    for scoreContent in datas:
        content = scoreContent.content
        content = content.lower().replace(" ", "")
        cutContent = cut_sentence_short(content)
        max_score = -1
        max_len = -1
        for con in cutContent:
            score = fuzzSimilarity(question, con)
            length = longestLen(question_anal, con)
            max_score = max(max_score, score)
            max_len = max(max_len, length)
        cnt = 0
        exist_words = 0
        for word in question_analysisCut:
            count = filter(content, word)
            if count != 0:
                exist_words += 1
            cnt += count
        quesSize = len(question_analysisCut)
        if quesSize == 0:
            scoreContent.words_ratio = 1.0
        else:
            scoreContent.words_ratio = exist_words / quesSize * max_len
        scoreContent.fuzz_score = max_score
    return es_sorted(datas)


def init_question_template(file_path):
    question_template = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            # 去除行尾的换行符
            line = line.strip()
            question_template.append(line)
    for i, line in enumerate(question_template):
        patterns.append(re.compile(line))


def merge(intervals):
    intervals.sort(key=lambda x: x[0])
    res = []
    for i in range(len(intervals)):
        l, r = intervals[i][0], intervals[i][1]
        if len(res) == 0 or res[-1][1] < l:
            res.append([l, r])
        else:
            res[-1][1] = max(res[-1][1], r)
    return res


def question_analysis(question):
    find = False
    query = question.replace("，", "")
    matchIndex = []
    for i in range(patternsLen):
        regex = patterns[i]
        matcher = re.search(regex, query)
        if matcher is not None:
            find = True
            for match in re.finditer(regex, query):
                start = match.start()
                end = match.end()
                matchIndex.append([start, end])
    if find:
        mergeIndex = merge(matchIndex)
        res = []
        startI = 0
        for i in range(len(mergeIndex)):
            if startI != mergeIndex[i][0]:
                res.append(query[startI:mergeIndex[i][0]])
            startI = mergeIndex[i][1]
        if mergeIndex[-1][1] < len(query):
            res.append(query[mergeIndex[-1][1]:])
        return ''.join(res)
    return query


def fuzzSimilarity(question, content):
    similarityScore = fuzz.token_sort_ratio(question, content)
    return similarityScore


def cut_sentence_short(content):
    regex = "[。！!?？;；]"
    cons = re.split(regex, content)
    return cons


def zeros(context_char_idxs):
    for i in range(len(context_char_idxs)):
        for j in range(len(context_char_idxs[i])):
            context_char_idxs[i][j] = 0
    return context_char_idxs


def longestLen(question_analysis, content):
    q_len = len(question_analysis)
    c_len = len(content)
    dp = [[0] * (c_len + 1) for _ in range(q_len + 1)]
    dp = zeros(dp)
    ques_char = list(question_analysis)
    con_char = list(content)
    for i in range(1, q_len + 1):
        for j in range(1, c_len + 1):
            if ques_char[i - 1] == con_char[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp[q_len][c_len]


def filter(string, sub_str):
    index = 0
    count = 0
    while True:
        index = string.find(sub_str, index)
        if index == -1:
            break
        index += 1
        count += 1
    return count


def es_sorted(datas):
    sorted_compare(datas)
    return datas


def sorted_compare(datas):
    datas.sort(key=lambda o: (o.words_ratio, o.fuzz_score))
    datas.reverse()
    return datas
