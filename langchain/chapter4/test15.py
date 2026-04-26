import os
# 配置 HuggingFace 国内镜像源
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'
os.environ['HF_HUB_DISABLE_TELEMETRY'] = '1'

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

# 使用在线模型（首次运行会自动下载）
embedding_model_name = "BAAI/bge-small-zh-v1.5"  # 中文效果好，体积小

# 初始化本地CPU运行的嵌入模型
# 字典参数传递
embeddings = HuggingFaceEmbeddings(
    model_name=embedding_model_name, # 模型路径本地或者HuggingFace仓库
    model_kwargs={ # 传递给底层模型加载器的参数
        "device": "cpu",  # 强制CPU运行，无需GPU
        # 如需加载量化模型，可添加以下配置（按需）
        # "trust_remote_code": True,
        # "load_in_8bit": False
    },
    # 传递给编码函数的参数
    encode_kwargs={
        "normalize_embeddings": True  # 归一化向量，提升检索效果
    }
)

# 加载已有的FAISS向量数据库
# 类方法调用
vector_db = FAISS.load_local(
    folder_path="./faiss_db",  # 之前存储向量的路径
    embeddings=embeddings,
    allow_dangerous_deserialization=True
)
print("向量数据库加载成功！")