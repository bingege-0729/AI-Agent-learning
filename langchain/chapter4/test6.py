from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableWithFallbacks
from langchain_openai import ChatOpenAI
from langchain_core.exceptions import OutputParserException
import os
import httpx
from dotenv import load_dotenv

load_dotenv()

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

core_llm = ChatOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("BASE_URL"),
    model="qwen-turbo",
    temperature=0.3,
    http_client=http_client
)

# .from_messages([])类方法调用，[]列表包含两个元组
core_prompt = ChatPromptTemplate.from_messages([
    ("system", "用专业语言详细解答用户问题。"),
    ("human", "{query}")
])

# 管道操作符
# core_chain是一个Runnable对象
core_chain = core_prompt | core_llm | StrOutputParser()

# 2️⃣ 降级链（稳定但精度略低）
fallback_llm = ChatOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("BASE_URL"),
    model="qwen-turbo",
    temperature=0.3,
    http_client=http_client
)
fallback_prompt = ChatPromptTemplate.from_messages([
    ("system", "用简洁语言解答用户问题，保证信息准确。"),
    ("human", "{query}")
])
fallback_chain = fallback_prompt | fallback_llm | StrOutputParser()

# 3️⃣ 构建带降级的链
# 声明变量类型为RunnableWithFallbacks
# 这是一个包装类型，包含猪脸和降级链
# .with_fallbacks()在Runnable对象上调用实例方法返回一个新的RunnableWithFallbacks对象
# 不修改原对象，而是创建新对象（不可变性）
chain_with_fallback: RunnableWithFallbacks = core_chain.with_fallbacks(
    # 列表
    # 可以传入多个降级链
    # 按列表顺序依次尝试
    fallbacks=[fallback_chain],
    exceptions_to_handle=(ConnectionError, TimeoutError),# ✅ 官方推荐：只捕获临时错误或网络错误
)

# 4️⃣ 调用链并捕获异常
try:
    result = chain_with_fallback.invoke({"query": "什么是RAG技术？"})
    print("解答：", result)
except OutputParserException as e:
    print(f"解析失败：{e}")
except Exception as e:
    print(f"最终失败：{e}")
