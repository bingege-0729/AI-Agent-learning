# LangChain 学习示例

这个目录包含了我学习 LangChain 的示例代码和笔记，主要聚焦于记忆管理和 Agent 应用。

## 📁 目录结构

```
langchain/
└── chapter3/                   # 第三章：记忆与代理
    ├── test1.py                # 全量记忆示例
    ├── test2.py                # 窗口记忆示例
    ├── test3.py                # 摘要记忆示例
    ├── test4.py                # 基础 Agent 示例
    ├── test5.py                # 带参数验证的 Agent 示例
    ├── test6.py                # 文件管理 Agent 示例
    ├── Calculator.py           # 计算器工具
    └── FileCon.py              # 文件连接工具
```

## 🚀 快速开始

### 环境准备

1. 确保已安装 Python 3.8+
2. 安装必要的依赖包：
   ```bash
   pip install langchain langchain-openai langchain-community langgraph python-dotenv pydantic
   ```

3. 配置环境变量：
   在项目根目录创建 `.env` 文件，添加以下内容：
   ```env
   OPENAI_API_KEY=your_api_key_here
   BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
   ```

### 运行示例

进入 chapter3 目录后，每个测试文件都可以独立运行：
```bash
cd chapter3

# 运行全量记忆示例
python test1.py

# 运行窗口记忆示例
python test2.py

# 运行摘要记忆示例
python test3.py

# 运行基础 Agent 示例
python test4.py

# 运行带参数验证的 Agent 示例
python test5.py

# 运行文件管理 Agent 示例
python test6.py
```

## 📖 文件说明

### chapter3 - 记忆与代理

#### test1.py - 全量记忆示例

演示如何实现完整对话历史的记忆：
- 使用 InMemoryChatMessageHistory 存储对话
- 通过 RunnableWithMessageHistory 管理会话
- 保留所有历史消息，支持跨长对话的上下文引用

**关键点**：
- 适用于需要记住所有历史信息的场景
- 使用 `MessagesPlaceholder` 在提示词中注入历史
- 通过 `get_full_memory_history` 函数管理会话存储

#### test2.py - 窗口记忆示例

演示滑动窗口记忆机制：
- 只保留最近 N 轮对话
- 自动截断旧消息以节省 token
- 验证窗口截断效果

**关键点**：
- 适用于只需要关注最近对话的场景
- 通过 `WINDOW_SIZE` 控制保留的轮数
- 当历史超过阈值时自动截断

#### test3.py - 摘要记忆示例

演示如何使用摘要压缩对话历史：
- 自动生成对话摘要
- 将摘要注入到提示词中
- 平衡记忆完整性和 token 消耗

**关键点**：
- 使用 RunnablePassthrough.assign 动态添加摘要
- 摘要链和对话链分离，便于管理
- 适合长对话场景，有效减少 token 使用

#### test4.py - 基础 Agent 示例

演示如何创建简单的 Agent：
- 使用 @tool 装饰器定义工具
- 实现天气查询功能
- 展示 Agent 自动调用工具的能力

**关键点**：
- `@tool` 装饰器快速创建工具
- Agent 自动判断何时调用工具
- 工具的文档字符串会被用于提示词

#### test5.py - 带参数验证的 Agent 示例

演示如何为工具添加参数验证：
- 使用 Pydantic 定义参数模型
- 实现温度单位转换工具
- 展示类型安全的工具调用

**关键点**：
- `args_schema` 参数指定参数模型
- Pydantic 提供类型验证和文档
- 参数描述帮助 Agent 正确使用工具

#### test6.py - 文件管理 Agent 示例

演示如何使用 FileManagementToolkit：
- 实现文件读写操作
- Agent 自动执行文件管理任务
- 展示复杂工具集成的能力

**关键点**：
- `FileManagementToolkit` 提供常用文件操作
- Agent 可以组合多个工具完成任务
- 支持指定工作目录

#### 工具模块

- `Calculator.py`: 计算器工具，提供基本的数学运算功能
- `FileCon.py`: 文件连接工具，用于文件操作和内容处理

## 📚 学习笔记

### 记忆管理

- **全量记忆**：保留所有历史消息，适合需要记住所有信息的场景
- **窗口记忆**：只保留最近 N 轮对话，节省 token 成本
- **摘要记忆**：通过压缩历史为摘要，平衡记忆完整性和 token 消耗

### Agent 应用

- **工具定义**：使用 `@tool` 装饰器快速创建工具
- **参数验证**：使用 Pydantic 定义参数模型，确保类型安全
- **工具集成**：支持多种工具组合，实现复杂任务

### 核心概念

- LangChain 是一个用于构建语言模型应用的框架
- 提供了各种工具和组件，方便构建复杂的应用
- 支持多种语言模型和工具集成
- 核心组件包括：模型、提示词模板、记忆管理、工具、Agent 等

## 📝 注意事项

1. 确保正确配置 `.env` 文件中的 API Key
2. 根据实际使用的模型调整 `model` 参数（如 qwen-plus、qwen-turbo 等）
3. 注意 API 调用的费用限制，合理使用记忆策略
4. 合理设置 `temperature` 参数，控制输出的随机性
5. 生产环境中建议使用数据库存储会话历史，而非内存存储
