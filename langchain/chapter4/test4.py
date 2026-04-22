from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.exceptions import OutputParserException
from langchain_core.runnables import Runnable
import os
import httpx
from langchain_openai import ChatOpenAI
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

llm = ChatOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("BASE_URL"),
    model="qwen-turbo",
    temperature=0.3,
    http_client=http_client
)

# 1️⃣ Prompt
summary_prompt = ChatPromptTemplate.from_messages([
    ("system", "请简洁总结以下文本核心内容，不超过50字。"),
    ("human", "{text}")
])

# 2️⃣ 基础链
base_chain: Runnable = summary_prompt | llm | StrOutputParser()

# 3️⃣ 重试链（官方推荐：直接 with_retry）
retry_chain = base_chain.with_retry( # 调用with_retry 方法
    stop_after_attempt=3,          # 最多重试 3 次
    wait_exponential_jitter=True,  # 指数退避 + 抖动（推荐）
    retry_if_exception_type=(
        ConnectionError,           # 链接错误时重试
        TimeoutError,              # 超时错误时重试
    ),
)

# 4️⃣ 调用
# 多层异常捕获
try:
    result = retry_chain.invoke({
        "text": "LangChain是一个用于构建大模型应用的框架，提供了丰富的Runnable组件，支持重试、降级等工程化能力。"
    })
    print("总结结果：", result)

except OutputParserException as e:
    # ❗ 解析错误通常是逻辑问题，不建议重试
    print("输出解析失败：", e)

except Exception as e:
    print("最终失败（已达到最大重试次数）：", e)

# 学到重试机制（解决零食API错误）