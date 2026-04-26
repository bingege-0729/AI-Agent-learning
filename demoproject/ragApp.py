import os
# 配置 HuggingFace 国内镜像源
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'
os.environ['HF_HUB_DISABLE_TELEMETRY'] = '1'

from langchain_community.document_loaders import (
    PyPDFLoader,
    UnstructuredPowerPointLoader,
    Docx2txtLoader
)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.chat_models import ChatTongyi
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# === 1. 自动加载指定文件夹下所有 PDF/PPT/DOCX ===
def load_documents_from_folder(folder_path):
    documents = []
    for filename in os.listdir(folder_path):
        filepath = os.path.join(folder_path, filename)
        if filename.endswith(".pdf"):
            loader = PyPDFLoader(filepath)
            docs = loader.load()
        elif filename.endswith((".ppt", ".pptx")):
            loader = UnstructuredPowerPointLoader(filepath)
            docs = loader.load()
        elif filename.endswith(".docx"):
            loader = Docx2txtLoader(filepath)
            docs = loader.load()
        else:
            continue
        documents.extend(docs)
        print(f"✅ 已加载: {filename}")
    return documents

# 加载你的知识库文件（放在 ./docs 文件夹中）
docs = load_documents_from_folder("./docs")
text_splitter = RecursiveCharacterTextSplitter(

    chunk_size=500,
    chunk_overlap=50,
    separators=["\n\n", "\n", "。", "！", "？", "；", " ", ""]
)
# 拆分文档，使用text_splitter 对文档进行拆分,split_documents()是用于将文档进行拆分，返回一个列表，列表中的元素是拆分后的文档对象。
splits = text_splitter.split_documents(docs)

# === 3. 向量化（使用中文友好模型）===
embedding = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-zh-v1.5",  # 中文效果好，支持离线
    model_kwargs={'device': 'cpu'}  # 若有 GPU 可改为 'cuda'
)

# === 4. 构建向量数据库 ===
vectorstore = Chroma.from_documents(
    documents=splits,
    embedding=embedding,
    persist_directory="./chroma_db"  # 持久化到本地
)
vectorstore.persist()

# === 5. 设置检索器 ===
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# === 6. 使用云端大模型（阿里云通义千问）===
# 从环境变量获取 API Key
import dotenv
dotenv.load_dotenv()

openai_api_key= os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    print("❌ 未找到 DASHSCOPE_API_KEY 环境变量")
    print("\n请在项目根目录创建 .env 文件，添加：")
    print("DASHSCOPE_API_KEY=your-api-key-here")
    exit(1)

llm = ChatTongyi(
    model="qwen-plus",  # 可选: qwen-turbo, qwen-plus, qwen-max
    dashscope_api_key=openai_api_key,
    temperature=0.5
)

# === 7. 构建 RAG 链（使用新式 API）===
# 定义提示词模板（符合 RAG 回答规范）
template = """你是一个专业的知识库助手。请基于以下上下文信息回答问题。

回答要求：
1. 优先使用上下文中的信息
2. 分点说明，结构清晰
3. 结合具体案例或示例
4. 如果上下文中没有相关信息，请明确说明

上下文信息：
{context}

用户问题：{question}

请给出详细回答："""

prompt = ChatPromptTemplate.from_template(template)

# 构建检索增强生成链
def format_docs(docs):
    return "\n\n".join([doc.page_content for doc in docs])

rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# === 8. 持续对话模式 ===
print("RAG 智能问答系统已启动（输入 'q' 退出）\n")

while True:
    # 获取用户输入
    query = input("请输入问题: ").strip()
    
    # 检查是否退出
    if query.lower() in ['quit', 'exit', 'q', '退出']:
        print("再见！")
        break
    
    # 检查是否为空输入
    if not query:
        print("⚠️  问题不能为空，请重新输入")
        continue
    
    # 生成回答
    try:
        result = rag_chain.invoke(query)
        print(f"\n{result}\n")
    except Exception as e:
        print(f"错误: {str(e)}")