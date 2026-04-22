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
# 1️⃣ 定义多变量 Prompt 链（营销话术生成示例）
# ChatPromptTemplate.from_messages([])
# 调用类方法(classmethod)，[]列表包含两个元组
marketing_prompt = ChatPromptTemplate.from_messages([
    ("system", "根据产品卖点和目标人群，撰写一句营销话术。"),
    ("human", "产品卖点：{sell_points}，目标人群：{target_audience}")
])

# 2️⃣ 构建链
# 类型注解，声明变量类型
marketing_chain: Runnable = marketing_prompt | llm | StrOutputParser()

# 3️⃣ 调用并捕获异常（官方推荐风格）
# 字典，键值对
inputs = {
    "sell_points": "无线耳机续航30小时",
    # "target_audience" 故意缺失，用于演示 KeyError
}
# 异常处理
try:
    # 可能抛出异常的代码
    # 调用对象的invoke方法，marketing_chain为一个Runnable的对象，支持统一的调用接口
    result = marketing_chain.invoke(inputs)
    print("营销话术：", result)

except KeyError as e:
    # 处理该异常的代码
    # 抛出 KeyError 异常，直接提取缺失的变量名
    missing_var = str(e).strip("'\"")
    # 把异常对象转换为字符串，取出字符串两端的单引号和双引号
    # f-string，格式化字符串
    print(f"错误提示：缺少必要输入变量 [{missing_var}]，请检查输入数据是否完整。")
except OutputParserException as e:
    # 官方推荐：逻辑解析错误不重试
    print(f"解析失败：{e}，请确认 Prompt 与输出格式匹配。")

except Exception as e:
    # ❗ 兜底捕获未知异常
    #type(e).__name__ 动态获取异常对象名称
    print(f"未知错误：{type(e).__name__}: {e}，请联系开发者排查。")

# 本案例最后会出现缺少输入变量“target_audience”的报错
# 错误提示：缺少必要输入变量 [Input to ChatPromptTemplate is missing variables {'target_audience'}.  Expected: ['sell_points', 'target_audience'] Received: ['sell_points']\nNote: if you intended {target_audience} to be part of the string and not a variable, please escape it with double curly braces like: '{{target_audience}}'.\nFor troubleshooting, visit: https://docs.langchain.com/oss/python/langchain/errors/INVALID_PROMPT_INPUT ]，请检查输入数据是否完整。
# 优先处理KeyError的错误