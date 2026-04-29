# NotRequired 来自 Python 的 typing 模块扩展，它是 PEP 655 引入的特性
# NotRequired 从 Python 3.11 开始内置支持
# from typing import TypedDict, NotRequired

#如果你使用的是 Python ≤3.10，需要安装 typing_extensions：
# pip install typing_extensions
from typing import TypedDict
from typing_extensions import NotRequired
# TypedDict为强类型字典，提供编译时类型检查

from typing import TypedDict, NotRequired

# ====== 全局共享状态（黑板） ======
class TaskState(TypedDict):
    user_query: str #用户原始查询
    intent: NotRequired[str] #用户意图
    llm_answer: NotRequired[str] #LLM 生成的回答
    tool_result: NotRequired[str] #工具调用结果
    final_answer: NotRequired[str] #最终回答
    progress: NotRequired[int] #任务进度百分比


class TaskState(TypedDict):
    user_query: str #用户原始查询
    tool_result: NotRequired[str] #工具调用结果
    final_answer: NotRequired[str] #最终回答
    progress: NotRequired[int] #任务进度百分比
# NotRequired[T] 表示非必须字段
# 运行时还是普通dict，访问时用state["key"]

# ======节点函数=========
# 接收完整状态对象state: TaskState
# 返回值：返回部分更新字典（不是完整状态）
def parse_query(state: TaskState):
    print("\n====== 节点1 parse_query 输入状态 ======")
    print(state)

    query = state["user_query"]
    update = {
        "tool_result": f"已解析问题: {query}",
        "progress": 30
    }

    print("------ 节点1 更新字段 ------")
    print(update)

    return update


def call_tool(state: TaskState):
    print("\n====== 节点2 call_tool 输入状态 ======")
    print(state)

    result = f"工具搜索结果：关于『{state['user_query']}』的相关知识"
    update = {
        "tool_result": result,
        "progress": 70
    }

    print("------ 节点2 更新字段 ------")
    print(update)

    return update


def generate_answer(state: TaskState):
    print("\n====== 节点3 generate_answer 输入状态 ======")
    print(state)

    answer = f"最终回答：基于工具结果 -> {state['tool_result']}"
    update = {
        "final_answer": answer,
        "progress": 100
    }

    print("------ 节点3 更新字段 ------")
    print(update)

    return update

#========构建 LangGraph 工作流======
from langgraph.graph import StateGraph

# 1. 创建图（绑定状态类型）
builder = StateGraph(TaskState)# 指定状态类型，泛型约束


# 2. 添加节点
builder.add_node("parse_query", parse_query)
builder.add_node("call_tool", call_tool)
builder.add_node("generate_answer", generate_answer)

# 3. 定义执行顺序（边）
builder.set_entry_point("parse_query")
builder.add_edge("parse_query", "call_tool")
builder.add_edge("call_tool", "generate_answer")

# 4. 编译图
graph = builder.compile()

# ====== 运行工作流 ======
init_state = TaskState(user_query="什么是 LangGraph？")

final_state = graph.invoke(init_state)

print("\n最终状态：")
print(final_state)

# 初始白板:
# ┌─────────────────────────┐
# │ user_query: "什么是LangGraph?" │
# └─────────────────────────┘
#
# ↓ parse_query 节点执行(只写自己负责的部分)
# ┌─────────────────────────┐
# │ user_query: "什么是LangGraph?" │  ← 保持不变
# │ tool_result: "已解析问题..."  │  ← 新增
# │ progress: 30                │  ← 新增
# └─────────────────────────┘
#
# ↓ call_tool 节点执行(覆盖部分字段)
# ┌──────────────────────────────────┐
# │ user_query: "什么是LangGraph?"        │  ← 保持不变
# │ tool_result: "工具搜索结果..."       │  ← 被覆盖
# │ progress: 70                       │  ← 被覆盖
# └──────────────────────────────────┘
#
# ↓ generate_answer 节点执行
# ┌──────────────────────────────────┐
# │ user_query: "什么是LangGraph?"     │  ← 保持不变
# │ tool_result: "工具搜索结果..."       │  ← 保持不变
# │ progress: 100                      │  ← 被覆盖
# │ final_answer: "最终回答..."         │  ← 新增
# └──────────────────────────────────┘