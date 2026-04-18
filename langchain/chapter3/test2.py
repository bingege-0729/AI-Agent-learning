import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough
from langchain_core.chat_history import BaseChatMessageHistory, InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI

# 加载环境变量（确保.env文件中配置了API_KEY）
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")
BASE_URL = os.getenv("BASE_URL")

# 初始化LLM模型
llm = ChatOpenAI(
    api_key=str(API_KEY) if API_KEY else "",
    base_url=str(BASE_URL) if BASE_URL else "",
    model="qwen-plus",
    temperature=0.3  # 降低随机性，保证输出稳定
)


# 定义提示词模板（包含历史消息占位符）

window_memory_prompt = ChatPromptTemplate.from_messages([
    ("system","你是友好的对话助手，需基于完整的历史对话回答用户问题。"),
    MessagesPlaceholder(variable_name="chat_history"), # 历史消息占位符
    ("human","{user_input}")
])

window_base_chain=window_memory_prompt | llm

window_memory_store = {}
WINDOW_SIZE = 2
def get_window_memory_history(session_id :str)->BaseChatMessageHistory:
    """获取会话历史，保留最近WINDOW_SIZE条消息"""
    if session_id not in window_memory_store:
       window_memory_store[session_id]=InMemoryChatMessageHistory()

    history = window_memory_store[session_id]

    if len(history.messages) >2*WINDOW_SIZE:
        history.messages = history.messages[-2*WINDOW_SIZE:]
    return history

window_memory_chain = RunnableWithMessageHistory(
    runnable=window_base_chain,
    get_session_history=get_window_memory_history,
    input_messages_key="user_input",# 输入中用户问题的键名
    history_messages_key="chat_history"# 传入提示词的历史消息键名
)

# 测试多轮对话（session_id=user_002，与全量记忆会话隔离）
config = {"configurable": {"session_id": "user_002"}}

# 模拟5轮对话，验证窗口记忆的截断效果
inputs = [
    "我叫小红",
    "我喜欢画画",
    "我来自上海",
    "我是一名学生",
    "我刚才说我来自哪里？",  # 第5轮：询问第3轮的信息，验证窗口截断
    "我叫什么名字？"  # 第6轮：询问第1轮的信息，验证窗口记忆
]

for i, user_input in enumerate(inputs, 1):
    response = window_memory_chain.invoke({"user_input": user_input}, config=config)
    print(f"\n第{i}轮 - 助手回复：", response.content)

# 查看窗口记忆的最终历史（仅保留最近2轮）
print("\n窗口记忆的最终对话历史（最近2轮）：")
for msg in get_window_memory_history("user_002").messages:
    print(f"{msg.type}: {msg.content}")