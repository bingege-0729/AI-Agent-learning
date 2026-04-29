
from typing import TypedDict
from typing_extensions import NotRequired
class TaskState(TypedDict):
    user_query: str #用户原始查询
    intent: NotRequired[str] #用户意图
    llm_answer: NotRequired[str] #LLM 生成的回答
    tool_result: NotRequired[str] #工具调用结果
    final_answer: NotRequired[str] #最终回答
    progress: NotRequired[int] #任务进度百分比
def route_by_intent(state: TaskState):
    if state.get("intent") == "summarize":
        return "summarize_node"
    else:
        return "rewrite_node"


builder = StateGraph(TaskState)

builder.add_node("parse_intent", parse_intent)
builder.add_node("summarize_node", summarize_node)
builder.add_node("rewrite_node", rewrite_node)
builder.add_node("final_node", final_node)

builder.set_entry_point("parse_intent")

# 条件边
builder.add_conditional_edges(
    "parse_intent",
    route_by_intent,
    {
        "summarize_node": "summarize_node",
        "rewrite_node": "rewrite_node",
    }
)

builder.add_edge("summarize_node", "final_node")
builder.add_edge("rewrite_node", "final_node")

graph = builder.compile()


print("\n====== 测试总结 ======")
print(graph.invoke(TaskState(user_query="请总结这段话")))

print("\n====== 测试改写 ======")
print(graph.invoke(TaskState(user_query="请改写这段话")))
