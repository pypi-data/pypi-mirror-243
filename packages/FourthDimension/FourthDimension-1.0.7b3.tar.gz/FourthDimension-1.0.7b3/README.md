# 工具介绍
FourthDimension（第四维度）由华中科技大学人工智能与嵌入式实验室联合言图科技研发，是一款基于大语言模型的智能检索增强生成（RAG）系统，提供私域知识库、文档问答等多种服务。此外，FourthDimension提供便捷的本地部署方法，方便用户在本地环境中搭建属于自己的应用平台。

### 工具特点
支持在线调用和本地部署，可选装不同的Embedding模型和答案生成模型，支持构建私域知识库，实现知识库问答。

### 主要服务
* 私域知识库
* 知识库问答
* 向量存储与检索
* 检索增强生成

# 工具使用

### 前置依赖项
- Anaconda3  

> 使用前请检查Anaconda是否安装，若未安装可参照以下教程进行安装。  
> [Anaconda详细安装过程](https://blog.csdn.net/weixin_43858830/article/details/134310118?csdn_share_tail=%7B%22type%22%3A%22blog%22%2C%22rType%22%3A%22article%22%2C%22rId%22%3A%22134310118%22%2C%22source%22%3A%22weixin_43858830%22%7D)

### 快速上手

1. 克隆项目Gitee库
```
mkdir FourthDimension
cd FourthDimension
git clone https://gitee.com/hustai/FourthDimension ./
```
2. 创建Conda虚拟环境
> python版本号要求 >= 3.8.1 ,<4.0
```
conda create -n FourthDimension python==3.8.1
conda activate FourthDimension
```
3. 安装FourthDimension  
3.1 安装前置依赖
```
pip install -r dependency.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;3.2 安装FourthDimension 
```
sh FourthDimension.sh install
```

4. 启动FourthDimension
> 如需重启服务请将start参数替换为restart
```
sh FourthDimension.sh start
```

5. FourthDimension示例代码  
> 运行示例程序，实现文档导入私域知识库，基于私域知识库的问答（检索增强生成）
```text
python example/demo.py
```

6. FourthDimension使用说明  

>config.json为FourthDimension的配置文件，在使用FourthDimension时请将config.json置于脚本文件同级目录下

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;6.1 导入文档到私域知识库
```text
import FourthDimension  

# 传入文档路径或文件夹路径，目前支持的文档类型包括doc、docx等
result = FourthDimension.upload('./data/example/')
print(result)
```
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;6.2 基于私域知识库的问答（检索增强生成）
```text
import FourthDimension

# 传入问题“什么是活期存款”
answer = FourthDimension.query('什么是活期存款')
print(answer)
```
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;6.3 清空私域知识库
```text
import FourthDimension

result = FourthDimension.clean()
print(result)
```
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;6.4 config.json配置文件示例

```text
{
  "word_storage": "default",
  "embedding_storage": "faiss",
  "search_select": "default",
  "embedding_model": "bge-large-zh-v1.5",
  "answer_generation_model": "gpt-3.5-turbo-16k",
  "openai": {
    "api_key": "",
    "url": "https://api.openai.com/v1"
  },
  "para_config": {
    "chunk_size": 500,
    "overlap": 20
  },
  "recall_config": {
    "top_k": 10
  }
}
```
> 以下为config.json配置文件中各参数的说明
```text
word_storage：文档文本存储方式
embedding_storage：文档向量存储方式
search_select：检索方式
embedding_model：Embedding模型
answer_generation_model：答案生成模型
openai.api_key：配置您的api key
openai.url： 默认使用openai官方接口，可根据需求进行修改
para_config.chunk_size：文档切分段落长度
para_config.overlap：文档切分重叠度
recall_config.top_k：指定使用多少召回结果进行答案生成
```


# 论坛交流


# 相关知识

- <a href="https://hustai.gitee.io/zh/posts/rag/RetrieveTextGeneration.html" target="_blank">基于检索增强的文本生成</a>

- <a href="https://hustai.gitee.io/zh/posts/rag/LLMretrieval.html" target="_blank">如何通过大模型实现外挂知识库优化</a>

<a href="https://hustai.gitee.io/zh/" target="_blank">更多相关知识分享——网站链接</a>


