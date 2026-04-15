from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY=os.getenv('OPENAI_API_KEY')
BASE_URL=os.getenv('BASE_URL')

if not API_KEY:
    raise ValueError("未检测到API_KEY，请检查 .env文件是否匹配正确")

chat_model = ChatOpenAI(
    api_key=API_KEY,
    base_url=BASE_URL,
    model="qwen-turbo",
    temperature=0.5,
    max_tokens=50
)

# 初始化对话历史（包含System）
history = [
    {"role": "system","content":"你是一个耐心的AI学习助手，回复简洁易懂，适合高校学生理解。"},

]
history.append({"role":"user","content":"请用3句话解释什么是LangChain"})

result = chat_model.invoke(history)
print("[第一轮对话]：")
print(result.content)


history.append({"role":"assistant","content":result.content})

# 第二轮对话
# 追问

history.append({"role":"user","content":"核心组件有哪些？"})

result = chat_model.invoke(history)

print("\n[第二轮对话]：")
print(result.content)


history.append({"role":"assistant","content":result.content})
history.append({"role":"user","content":"给我做一个简单使用场景"})

result = chat_model.invoke(history)

print("\n[第三轮对话]：")
print(result.content)