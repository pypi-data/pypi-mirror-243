import json
from typing import Union
import faiss
import jieba
import numpy as np
from FourthDimension.config.config import embedding_model


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    f.close()
    return data


def write_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json_data = json.dumps(data, ensure_ascii=False, indent=4)
        f.write(json_data)
    f.close()


def chinese_segment(text):
    sentences = []
    seg_list = jieba.cut(text, cut_all=False)
    sentence = []
    for word in seg_list:
        sentence.append(word)
        if word in ['。', '？', '！']:
            sentences.append("".join(sentence))
            sentence = []
    if sentence:
        sentences.append("".join(sentence))
    return sentences

def index_search(query_embed, context_embed):
    contexts_embeddings = np.array([context_embed]).astype("float32")
    index = faiss.IndexFlatL2(contexts_embeddings.shape[1])  # 创建Faiss索引
    index.add(contexts_embeddings)
    query_embedding = np.array([query_embed]).astype("float32")
    D, I = index.search(query_embedding, 1)
    return D


def get_simi_score(question, context):
    query_embed = embedding_model.embed_query(question)
    contexts_embed = embedding_model.embed_query(context)
    D = index_search(query_embed=query_embed, context_embed=contexts_embed)
    return D
