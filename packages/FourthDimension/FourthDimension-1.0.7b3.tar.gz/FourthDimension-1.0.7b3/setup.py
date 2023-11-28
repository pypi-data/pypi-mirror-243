from setuptools import setup, find_packages

VERSION = '1.0.7b3'
DESCRIPTION = 'FourthDimension（第四维度）由华中科技大学人工智能与嵌入式实验室联合言图科技研发，是一款基于大语言模型的智能检索增强生成（RAG）系统，提供私域知识库、文档问答等多种服务。此外，FourthDimension提供便捷的本地部署方法，方便用户在本地环境中搭建属于自己的应用平台。'

setup(
    name="FourthDimension",
    version=VERSION,
    author="yantu-tech",
    author_email="wu466687121@qq.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=open('README.md', encoding="UTF8").read(),
    package_dir={"": "src"},
    packages=find_packages("src"),
    include_package_data=True,
    package_data={'FourthDimension': ['config/question_regex.txt', 'cache/faiss_cache/temp.index']},
    install_requires=[],
    keywords=["python", "yantu"],
    license="MIT",
    url="https://gitee.com/hustai/FourthDimension"
)
