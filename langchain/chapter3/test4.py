from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

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


@tool
def weather_query(city: str)->str:
    """查询指定城市的天气"""
    weather_data={
        "北京":"北京今日天气晴，最高温度30度，最低温度20度",
        "上海":"上海今日天气多云，最高温度28度，最低温度22度",
        "广州":"广州今日天气阴，最高温度32度，最低温度25度"
    }
    return weather_data.get(city,f"暂无{city}的天气信息")

tools= [weather_query]


agent = create_agent(
    model=llm,
    tools=tools,
    debug=True,
)

response = agent.invoke({
    "messages":[
        {"role":"user", "content":"我想知道广州的天气如何"}

    ]
})
print("\n最终回答：")
print(response["messages"][-1].content)