# LangChain 和 LangGraph 学习项目

这个项目是我学习 LangChain 和 LangGraph 的代码集合和笔记。

## 目录结构

```
langent-env/
├── langchain/                    # LangChain 学习示例
│   ├── chapter3/                 # 第三章：记忆与代理
│   │   ├── test1.py              # 全量记忆示例
│   │   ├── test2.py              # 窗口记忆示例
│   │   ├── test3.py              # 摘要记忆示例
│   │   ├── test4.py              # 基础 Agent 示例
│   │   ├── test5.py              # 带参数验证的 Agent 示例
│   │   ├── test6.py              # 文件管理 Agent 示例
│   │   ├── Calculator.py         # 计算器工具
│   │   └── FileCon.py            # 文件连接工具
├── langgraph/                    # LangGraph 学习示例
│   ├── chapter3/                 # 第三章示例
│   ├── README.md                 # LangGraph 学习说明
│   └── test1.py                  # LangGraph 基础示例
├── .env                          # 环境变量配置
├── .gitignore                    # Git 忽略文件
├── README.md                     # 项目说明（本文件）
└── requirements.txt              # 依赖列表
```

## 文件说明

### LangChain 目录

`langchain/` 目录包含 LangChain 学习示例和笔记，主要聚焦于记忆管理和 Agent 应用：

**chapter3 - 记忆与代理**：

- `test1.py`: 全量记忆示例
  - 演示如何实现完整对话历史的记忆
  - 使用 InMemoryChatMessageHistory 存储对话
  - 通过 RunnableWithMessageHistory 管理会话
  - 适用于需要记住所有历史信息的场景

- `test2.py`: 窗口记忆示例
  - 演示滑动窗口记忆机制
  - 只保留最近 N 轮对话
  - 自动截断旧消息以节省 token
  - 适用于只需要关注最近对话的场景

- `test3.py`: 摘要记忆示例
  - 演示如何使用摘要压缩对话历史
  - 自动生成对话摘要
  - 将摘要注入到提示词中
  - 平衡记忆完整性和 token 消耗

- `test4.py`: 基础 Agent 示例
  - 演示如何创建简单的 Agent
  - 使用 @tool 装饰器定义工具
  - 实现天气查询功能
  - 展示 Agent 自动调用工具的能力

- `test5.py`: 带参数验证的 Agent 示例
  - 演示如何为工具添加参数验证
  - 使用 Pydantic 定义参数模型
  - 实现温度单位转换工具
  - 展示类型安全的工具调用

- `test6.py`: 文件管理 Agent 示例
  - 演示如何使用 FileManagementToolkit
  - 实现文件读写操作
  - Agent 自动执行文件管理任务
  - 展示复杂工具集成的能力

**工具模块**：
- `Calculator.py`: 计算器工具
- `FileCon.py`: 文件连接工具

### LangGraph 目录

`langgraph/` 目录包含 LangGraph 学习示例和笔记：

- [查看 LangGraph 学习说明](langgraph/README.md)

**文件列表**：
- `test1.py`: LangGraph 基础示例
  - 演示如何构建简单的工作流
  - 展示图结构的工作流
  - 支持状态管理和节点之间的数据流

### 项目文件

- `.env`: 环境变量配置文件
  - OPENAI_API_KEY: API 密钥
  - BASE_URL: API 基础 URL
- `requirements.txt`: 项目依赖列表
- `.gitignore`: Git 忽略文件，指定不需要上传到远程仓库的文件和目录
- `README.md`: 项目说明文件（本文件）

## 环境设置

1. 克隆仓库后，创建虚拟环境：
   ```bash
   python -m venv .venv
   ```

2. 激活虚拟环境：
   - Windows (PowerShell):`.\Scripts\Activate.ps1`
   - Windows (CMD): `.venv\Scripts\activate.bat`
   - Linux/Mac: `source .venv/bin/activate`

3. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

4. 配置环境变量：
   创建 `.env` 文件并添加以下内容：
   ```
   OPENAI_API_KEY=your_api_key_here
   BASE_URL=your_base_url_here
   ```

## 运行示例

### LangChain 示例

```bash
# 进入 chapter3 目录
cd langchain/chapter3

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

### LangGraph 示例

```bash
# 进入 langgraph 目录
cd langgraph

# 运行 LangGraph 基础示例
python test1.py
```

## 学习资源

- [LangChain 官方文档](https://python.langchain.com/)
- [LangGraph 官方文档](https://langchain-ai.github.io/langgraph/)

## 注意事项

1. 本项目使用阿里云 DashScope 的 API，需要您自己申请 API Key
2. 请确保不要将 `.env` 文件上传到远程仓库，它已经在 `.gitignore` 中被排除
3. 如果您想使用其他模型，请修改代码中的 `model` 参数

## 许可证

本项目仅用于学习目的。