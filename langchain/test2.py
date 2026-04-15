from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
load_dotenv()

API_KEY=os.getenv('OPENAI_API_KEY')
BASE_URL=os.getenv('BASE_URL')

if not API_KEY:
    raise ValueError("未检测到API_KEY，请检查.env文件是否配置正确")

chat_model = ChatOpenAI(
    api_key=API_KEY,
    base_url=BASE_URL,
    model="qwen-turbo",
    temperature=0.5,
    max_tokens=200
)

message =[
    {"role": "system","content":"你是一个耐心的AI学习助手，回复简洁易懂，适合高校学生理解。"},
    {"role": "user","content":"请用3句话解释什么是LangChain"}
]


result = chat_model.invoke(message)

print("ChatModel回复：")
print(result.content)
