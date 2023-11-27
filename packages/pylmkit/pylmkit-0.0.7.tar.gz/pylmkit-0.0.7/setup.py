from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='pylmkit',  # 对外我们模块的名字
    author='52phm',  # 作者
    author_email='2374521450@qq.com',  # 作者邮箱
    version='0.0.7',  # 版本号
    description='pylmkit: Help users quickly build practical large model applications!',  # 项目摘要
    long_description=long_description,  # 项目介绍
    long_description_content_type="text/markdown",
    url="https://github.com/52phm/pylmkit",  # 程序主页地址
    packages=find_packages(),  # 要发布的模块
    license="Apache License-2.0",  # 协议（请注意按实际情况选择不同的协议），可选
    # 此处添加任意多个项目链接
    project_urls={
        # 英文关键字是内置好的关键字，有对应的logo
        "Homepage": "http://app.pylmkit.cn",
        "Documentation": "http://en.pylmkit.cn",
        # 也可以任意命名，默认统一logo
        "应用主页": "http://app.pylmkit.cn",
        "中文文档": "http://zh.pylmkit.cn",
    },
    install_requires=[
        'streamlit',
        'pyyaml',
        "dashscope",
        "zhipuai",
        "openai",
        "python-dotenv",
        'langchain',
        # 'duckduckgo_search',
        # "unstructured",
        # "pdf2image",
        # "pdfminer.six",
        # "sentence-transformers",
        # "faiss-cpu",
        # "websocket",
        # "chromadb",
    ]
)
