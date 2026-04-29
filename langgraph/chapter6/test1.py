from typing import TypedDict
from typing_extensions import NotRequired

class TaskState(TypedDict):
    user_query: str #用户原始查询
    tool_result: NotRequired[str] #工具调用结果
    final_answer: NotRequired[str] #最终回答
    progress: NotRequired[int] #任务进度百分比

#NotRequired 表示是非必须要求

def parse_query(state: TaskState):
    print("\n====== 节点1 parse_query 输入状态 ======")
    print(state)

    query = state["user_query"]
    update = {
        "tool_result": f"已解析问题: {query}",
        "progress": 30
    }

    return update

# 测试代码
if __name__ == "__main__":
    # 创建初始状态（只需提供必需的字段）
    initial_state = {
        "user_query": "如何学习Python编程？"
    }
    
    print("开始执行任务...")
    result = parse_query(initial_state)
    print("\n====== 函数返回结果 ======")
    print(result)