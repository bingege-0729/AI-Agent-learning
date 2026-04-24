# 配置 HuggingFace 镜像源(必须在导入前设置)
import os
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

# ==================== 语法详解 ====================
# 1. 模型路径变量定义
#    - 使用本地模型路径（相对路径或绝对路径）
#    - "./" 表示当前工作目录
embedding_model_name = "./models/Qwen/Qwen3-Embedding-0___6B"

# 2. 初始化嵌入模型
#    - HuggingFaceEmbeddings() 是类构造函数
#    - 参数使用关键字传参（keyword arguments）
embeddings = HuggingFaceEmbeddings(
    model_name=embedding_model_name,  # 模型名称/路径
    model_kwargs={                    # 字典类型参数：传递给底层模型
        "device": "cpu",              # 强制CPU运行（可选值："cpu", "cuda", "mps"）
        # 如需加载量化模型，可添加以下配置（按需）
        # "trust_remote_code": True,  # 信任远程代码（某些模型需要）
        # "load_in_8bit": False       # 8位量化加载（节省显存）
    },
    encode_kwargs={                   # 字典类型参数：传递给编码函数
        "normalize_embeddings": True  # 归一化向量（提升余弦相似度计算准确性）
    }
)

# 3. 加载已有的FAISS向量数据库
#    - load_local() 是类方法（class method）
#    - 必须提供与保存时相同的 embeddings 实例
vector_db = FAISS.load_local(
    folder_path="./faiss_db",                    # 向量库文件夹路径
    embeddings=embeddings,                       # 嵌入模型实例
    allow_dangerous_deserialization=True         # 允许反序列化（仅信任自己生成的文件）
)
print("✓ 向量数据库加载成功！")

# 4. 使用示例：相似性检索
query = "LangChain的链式工作流有哪些类型？"
retrieved_docs = vector_db.similarity_search(query, k=3)

print(f"\n与问题「{query}」最相关的文档：\n")
for i, doc in enumerate(retrieved_docs, 1):
    print(f"--- 片段 {i} ---")
    print(f"内容：{doc.page_content}")
    print(f"来源：{doc.metadata.get('source', '未知')}")
    print()
