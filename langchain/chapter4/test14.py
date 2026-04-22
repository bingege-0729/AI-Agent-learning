import os
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings

# 模块化设计：LangChain 将功能拆分为 community（社区维护，如 FAISS）、
# huggingface（模型集成）和 core（核心定义）。

# Document 类：这是 LangChain 中所有文档操作的“原子单位”，
# 包含 page_content（文本）和 metadata（元数据）。

txt_path = os.path.join("knowledge_base", "test.txt")
if not os.path.exists(txt_path):
    raise FileNotFoundError(f"文档文件不存在：{txt_path}")

# 加载文本文档
loader = TextLoader(txt_path, encoding="utf-8")
# 类型注解，可读性，IDE支持
txt_docs: list[Document] = loader.load()

# 文本分割（使用最新的 RecursiveCharacterTextSplitter 配置）
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,  # 每个文本块的大小
    chunk_overlap=50,  # 块之间的重叠长度（提升上下文连续性）
    length_function=len,  # 长度计算函数（中文用len即可）
    is_separator_regex=False  # 显式指定非正则分隔符（默认值，增加可读性）
    # 提高代码安全性，防止特殊字符被误解析为正则逻辑。
)
split_docs: list[Document] = text_splitter.split_documents(txt_docs)
print(f"分割后的文本片段数：{len(split_docs)}")

# 3. 初始化本地CPU运行的嵌入模型
# 使用 BAAI/bge-small-zh-v1.5，对中文支持好且体积小，首次运行会自动下载
embedding_model_name = "BAAI/bge-small-zh-v1.5"

embeddings = HuggingFaceEmbeddings(
    model_name=embedding_model_name,
    # 字典
    model_kwargs={
        "device": "cpu"  # 强制使用CPU运行，无需GPU
    },
    # 字典
    encode_kwargs={
        "normalize_embeddings": True  # 归一化向量，提升检索效果
        # 在使用余弦相似度
        # （Cosine Similarity）计算距离时，归一化后的向量计算更快、更准确。
    }
)

# 4. 构建并持久化FAISS向量库
try:
    # 生成向量并初始化FAISS（本地CPU计算，首次运行会下载模型，需联网）
    # .from_documents()这是一种工厂方法
    # 内部执行了内部自动执行了：
    # 遍历文档 -> 调用 Embedding 模型 -> 生成向量 -> 存入 FAISS 索引
    vector_db = FAISS.from_documents(
        documents=split_docs,
        embedding=embeddings,
    )

    # 持久化向量库到本地
    vector_db.save_local(
        folder_path="./faiss_db",
        index_name="local_cpu_faiss_index"  # 索引名改为本地CPU版
    )
    print("向量存储完成！向量数据已保存到 ./faiss_db 文件夹")
except Exception as e:
    raise RuntimeError(f"构建/保存向量库失败：{str(e)}")

# 5. 相似性检索测试
query = "LangChain的链式工作流有哪些类型？"
try:
    # 一次性获取带评分的检索结果
    # 元组解包
    # .similarity_search_with_score返回的是一个列表，每个元素是一个元组(Document, float)
    retrieved_docs_with_scores = vector_db.similarity_search_with_score(query, k=3)

    print(f"\n与问题「{query}」最相关的3个文本片段：")
    for i, (doc, score) in enumerate(retrieved_docs_with_scores):
        print(f"\n片段{i + 1}：")
        print(f"内容：{doc.page_content}")
        print(f"相关性评分（越小越相似）：{round(score, 4)}") # 保留4位小数
        print(f"来源：{doc.metadata.get('source', '未知')}") # 安全的字典访问 .get()
except Exception as e:
    raise RuntimeError(f"检索向量库失败：{str(e)}")


# graph LR
#     A[test.txt] --> B(TextLoader)
#     B --> C[List[Document]]
#     C --> D(RecursiveCharacterTextSplitter)
#     D --> E[Split Documents]
#     E --> F(HuggingFaceEmbeddings)
#     F --> G[Vector Vectors]
#     G --> H{FAISS Index}
#     H --> I[Save to Disk]
#     J[User Query] --> K(Embedding)
#     K --> H
#     H --> L[Top-K Results]

# 学习到4.4.4检索器配置与检索策略优化