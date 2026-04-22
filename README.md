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
│   ├── chapter4/                 # 第四章：RAG 检索增强生成
│   │   ├── knowledge_base/       # 知识库文件夹
│   │   ├── test7.py              # TXT 文档加载
│   │   ├── test8.py              # PDF 文档加载（PyPDFLoader）
│   │   ├── test9.py              # Word 文档加载
│   │   ├── test10.py             # 批量文档加载
│   │   ├── test11.py             # 文本拆分器配置
│   │   ├── test12.py             # Markdown 文档处理
│   │   ├── test13.py             # 向量库构建与检索
│   │   └── test14.py             # FAISS 向量库完整流程
│   ├── learning_method_example.json
│   ├── readme.md                 # LangChain 详细说明
│   └── test*.py                  # 其他测试文件
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

**chapter4 - RAG 检索增强生成**：

- `test7.py`: TXT 文档加载
  - 使用 TextLoader 加载纯文本文件
  - 演示 Document 对象的基本结构
  - 理解 page_content 和 metadata

- `test8.py`: PDF 文档加载
  - PyPDFLoader 基础用法（按页拆分）
  - PDFPlumberLoader 高级用法（保留表格）
  - 对比不同加载器的适用场景

- `test9.py`: Word 文档加载
  - 使用 Docx2txtLoader 加载 .docx 文件
  - 统一的 Document 接口设计

- `test10.py`: 批量文档加载
  - 遍历文件夹自动识别文件格式
  - 根据后缀选择对应的加载器
  - 异常处理和故障隔离

- `test11.py`: 文本拆分器配置
  - RecursiveCharacterTextSplitter 核心参数
  - chunk_size 和 chunk_overlap 的作用
  - 中文分隔符优化配置

- `test12.py`: Markdown 文档处理
  - UnstructuredMarkdownLoader 结构化加载
  - MarkdownTextSplitter 智能拆分
  - 保留标题层级关系

- `test13.py`: 向量库构建与检索
  - HuggingFace Embeddings 初始化
  - FAISS 向量库创建与持久化
  - 相似性检索测试

- `test14.py`: FAISS 向量库完整流程
  - 从文档加载到向量检索的完整链路
  - 本地 CPU 运行的嵌入模型
  - 带评分的检索结果展示

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

#### Chapter 3 - 记忆与代理

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

#### Chapter 4 - RAG 检索增强生成

```bash
# 进入 chapter4 目录
cd langchain/chapter4

# 运行 TXT 文档加载
python test7.py

# 运行 PDF 文档加载
python test8.py

# 运行 Word 文档加载
python test9.py

# 运行批量文档加载
python test10.py

# 运行文本拆分器配置
python test11.py

# 运行 Markdown 文档处理
python test12.py

# 运行向量库构建与检索
python test13.py

# 运行 FAISS 完整流程（首次运行会下载模型）
python test14.py
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

1. **API 配置**：本项目支持多种 API（阿里云 DashScope、DeepSeek、OpenAI 等），需要在 `.env` 中配置对应的 API Key
2. **隐私安全**：请确保不要将 `.env` 文件上传到远程仓库，它已经在 `.gitignore` 中被排除
3. **模型选择**：如果您想使用其他模型，请修改代码中的 `model` 参数
4. **RAG 模型下载**：首次运行 RAG 相关示例时，会自动下载 Embedding 模型（约 100MB），需要联网
5. **代理问题**：如遇到 SSL 或代理错误，请参考项目内的故障排查文档

## 许可证

本项目仅用于学习目的。