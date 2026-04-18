# LangGraph 学习示例

这个目录包含了我学习 LangGraph 的示例代码和笔记，主要聚焦于 Agent 应用。

## 📁 目录结构

```
langgraph/
├── chapter3/                   # 第三章示例
└── test1.py                    # LangGraph 基础示例
```

## 🚀 快速开始

### 环境准备

1. 确保已安装 Python 3.8+
2. 安装必要的依赖包：
   ```bash
   pip install langgraph langchain langchain-openai python-dotenv
   ```

3. 配置环境变量：
   在项目根目录创建 `.env` 文件，添加以下内容：
   ```env
   OPENAI_API_KEY=your_api_key_here
   BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
   ```

### 运行示例

```bash
# 运行 LangGraph 基础示例
python test1.py
```

## 📖 文件说明

### test1.py - LangGraph 基础示例

演示如何构建简单的工作流：
- 使用 @tool 装饰器定义工具
- 创建 Agent 并集成工具
- 展示图结构的工作流
- 支持状态管理和节点之间的数据流

**关键点**：
- `@tool` 装饰器用于定义可被 Agent 调用的工具
- `create_agent` 函数快速创建预配置的 Agent
- Agent 自动判断何时调用工具
- 支持调试模式，显示完整的执行过程

## 📚 学习笔记

### LangGraph 核心概念

- **有状态应用**：LangGraph 专为构建有状态的应用程序设计
- **图结构**：基于图的工作流，适合构建复杂的 AI 应用
- **状态管理**：支持状态管理和节点之间的数据流
- **与 LangChain 集成**：可以与 LangChain 无缝集成，使用其工具和组件

### Agent 应用

- **工具定义**：使用 `@tool` 装饰器快速创建工具
- **Agent 创建**：使用 `create_agent` 快速构建 Agent
- **自动执行**：Agent 自动判断何时调用工具
- **调试支持**：通过 `debug=True` 查看完整执行过程

## 📝 注意事项

1. 确保正确配置 `.env` 文件中的 API Key
2. 根据实际使用的模型调整 `model` 参数（如 qwen-plus、qwen-turbo 等）
3. 注意 API 调用的费用限制
4. 合理设置 `temperature` 参数，控制输出的随机性
5. 使用调试模式可以帮助理解 Agent 的决策过程
