from langchain_core.prompts import PromptTemplate
from langchain_community.chat_models import ChatTongyi
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os

# 1. 环境初始化
load_dotenv()
DASHSCOPE_API_KEY = os.getenv("OPENAI_API_KEY")  # ← 正确的环境变量名
if not DASHSCOPE_API_KEY:
    raise ValueError("未检测到 DASHSCOPE_API_KEY，请在 .env 中配置")

# 2. 初始化 Tongyi 模型（通义千问）
llm = ChatTongyi(
    dashscope_api_key=DASHSCOPE_API_KEY,
    model="qwen-turbo",        # 注意：全小写
    temperature=0.3,
    max_tokens=200
)

# 3. 创建解析器：将 AIMessage 转为 str
parser = StrOutputParser()

# 4. 构建链：模型 → 字符串解析
chain = llm | parser

# 5. 调用
result = chain.invoke("请简要介绍 LangChain 输出解析层的作用")

print("StrOutputParser 解析后的字符串：")
print(result)
print("\n解析结果类型：", type(result))  # 应该是 <class 'str'>