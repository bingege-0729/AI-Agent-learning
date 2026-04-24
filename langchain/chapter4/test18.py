from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI  # 1.x推荐用ChatOpenAI，适配对话模型，功能更全
from langchain_core.prompts import ChatPromptTemplate  # 替代PromptTemplate，适配LCEL
from langchain_core.runnables import RunnablePassthrough  # LCEL核心组件，传递数据
from langchain_core.output_parsers import StrOutputParser  # 统一输出格式解析
from dotenv import load_dotenv
import os
import httpx
import ssl

# 加载并验证环境变量（1.x推荐显式验证，避免配置缺失）
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
base_url = os.getenv("BASE_URL")

if not api_key:
    raise ValueError("未找到OPENAI_API_KEY环境变量，请检查.env文件配置")
if not base_url:
    raise ValueError("未找到BASE_URL环境变量，请检查.env文件配置")

# 配置SSL上下文（解决国内访问API的SSL问题）
try:
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
except Exception:
    ssl_context = None

http_client = httpx.Client(
    trust_env=False,
    verify=ssl_context if ssl_context else False
)

# 1. 初始化本地CPU运行的BGE嵌入模型（参数兼容1.x版本，保持原推荐配置）
embedding_model_path = "./models/BAAI/bge-small-zh-v1.5"
# 验证模型路径有效性
if not os.path.exists(embedding_model_path):
    raise FileNotFoundError(f"BGE嵌入模型路径不存在：{embedding_model_path}")

embeddings = HuggingFaceEmbeddings(
    model_name=embedding_model_path,
    model_kwargs={
        "device": "cpu",  # 强制CPU运行，无需GPU
    },
    encode_kwargs={
        "normalize_embeddings": True  # 归一化向量，提升检索相似度计算精度
    }
)

# 2. 加载FAISS向量数据库（1.x版本用法完全兼容，保留原逻辑）
# 注意：首次构建时需用FAISS.from_documents(docs, embeddings)创建并save_local
vector_db = FAISS.load_local(
    # load_local()是FAISS类的静态工厂方法，返回实例
    folder_path="./faiss_db",
    embeddings=embeddings,
    allow_dangerous_deserialization=True,  # 本地开发可用，生产环境需谨慎（存在安全风险）
    index_name="local_cpu_faiss_index"  # 确保加载正确的索引文件
)

# 3. 初始化检索器（MMR策略，平衡相关性和多样性，参数无变化）
retriever = vector_db.as_retriever(
    search_type="mmr",
    search_kwargs={"k": 3, "fetch_k": 10, "lambda_mult": 0.7}
)

# 4. 初始化大模型（1.x推荐用ChatOpenAI，支持更丰富的对话配置）
llm = ChatOpenAI(
    api_key=api_key,
    base_url=base_url,  # 必须指定API地址
    model="qwen-turbo",  # 指定模型名称
    temperature=0.3,  # 低温度保证答案精准，减少幻觉
    timeout=30,  # 新增超时配置，避免请求挂起（1.x官方推荐）
    max_retries=2,  # 网络波动时自动重试，提升稳定性
    http_client=http_client  # 使用自定义HTTP客户端（解决SSL问题）
)


# 1. 自定义文档格式化函数（将检索到的多个文档拼接为统一文本，供提示词使用）
def format_docs(docs):
    """格式化检索到的文档片段，用空行分隔"""
    return "\n\n".join([doc.page_content for doc in docs])

# 2. 自定义提示词模板（1.x推荐用ChatPromptTemplate，通过from_messages创建）
# 保持原业务规则：基于参考资料、分点说明、带案例
# 多行字符串“”“”“”
system_prompt = """你是一个专业的RAG系统问答助手，必须基于以下提供的参考资料（context）回答用户问题。
规则：
1. 答案必须严格基于参考资料，不能编造未提及的信息；
2. 语言简洁明了，分点说明（如果有多个要点）；
3. 每个要点搭配1个简单案例，帮助理解。

参考资料：{context}"""

custom_prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),  # 系统指令
    ("human", "{question}")     # 用户问题（1.x推荐用"question"键，语义更清晰）
])

# 3. 用LCEL构建完整检索-生成链（管道符串联组件，数据流式传递）
rag_qa_chain = (
    # 第一步：并行处理输入（传递用户问题+检索文档）
    {"context": retriever | format_docs, "question": RunnablePassthrough()},
    # 第二步：将格式化数据传入提示词模板
    custom_prompt,
    # 第三步：传入大模型生成答案
    llm,
    # 第四步：解析输出（统一为字符串格式）
    StrOutputParser()
)

# 补充：如需返回检索的源文档（用于验证答案来源），可调整链结构：
rag_qa_chain_with_sources = (
    {
        "context": retriever | format_docs,
        "question": RunnablePassthrough(),
        "source_documents": retriever  # 保留原始检索文档
    }
    | custom_prompt
    | llm
    | StrOutputParser()
)

# 测试问题列表（覆盖不同类型的查询）
test_questions = [
    "RAG系统的核心价值是什么？",
    "RAG和直接使用大模型相比，优势在哪里？",
    "企业内部知识库问答为什么适合用RAG？"
]

# 执行测试并打印结果
for i, question in enumerate(test_questions):
    print(f"\n===== 测试问题{i + 1}：{question} =====")
    # 执行RAG链（1.x统一用invoke方法）
    result = rag_qa_chain_with_sources.invoke(question)  # 带源文档的链

    # 打印生成的答案
    print("\n生成答案：")
    print(result)

    # 打印参考资料（验证答案来源）
    print("\n参考资料：")
    # 注意：源文档从链的输入参数中获取（因链结构中保留了source_documents）
    sources = retriever.invoke(question)  # 重新调用检索器获取源文档（或在链中传递）
    for j, doc in enumerate(sources):
        print(f"\n参考片段{j + 1}：")
        print(doc.page_content)
        if doc.metadata:  # 打印文档元数据（如文件名、页码等）
            print(f"元数据：{doc.metadata}")