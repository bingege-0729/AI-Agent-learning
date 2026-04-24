# LangChain 学习示例

这个目录包含了我学习 LangChain 的示例代码和笔记，涵盖记忆管理、Agent 应用和 RAG 检索增强生成。

## 📁 目录结构

```
langchain/
├── chapter3/                   # 第三章：记忆与代理
│   ├── test1.py                # 全量记忆示例
│   ├── test2.py                # 窗口记忆示例
│   ├── test3.py                # 摘要记忆示例
│   ├── test4.py                # 基础 Agent 示例
│   ├── test5.py                # 带参数验证的 Agent 示例
│   ├── test6.py                # 文件管理 Agent 示例
│   ├── Calculator.py           # 计算器工具
│   └── FileCon.py              # 文件连接工具
├── chapter4/                   # 第四章：RAG 检索增强生成
│   ├── knowledge_base/         # 知识库文件夹（存放测试文档）
│   ├── models/                 # 本地嵌入模型存储
│   ├── faiss_db/               # FAISS 向量数据库索引
│   ├── download_model.py       # 模型下载脚本
│   ├── rebuild_faiss.py        # FAISS 向量库重建脚本
│   ├── test7.py                # TXT 文档加载
│   ├── test8.py                # PDF 文档加载
│   ├── test9.py                # Word 文档加载
│   ├── test10.py               # Markdown 文档处理
│   ├── test11.py               # 批量文档加载
│   ├── test12.py               # 文本拆分器配置
│   ├── test13.py               # 向量库构建与检索
│   ├── test14.py               # FAISS 向量库完整流程
│   ├── test15.py               # FAISS 加载示例
│   ├── test15_load_faiss.py    # FAISS 加载详解版
│   ├── test16.py               # 多策略检索对比
│   ├── test17.py               # 检索器详细测试
│   └── test18.py               # LCEL RAG 链式调用（完整版）
├── learning_method_example.json
├── readme.md                   # 本文件
└── FAQ.md                      # 常见问题解答
```

## 🚀 快速开始

### 环境准备

1. 确保已安装 Python 3.9+
2. 安装必要的依赖包：
   ```bash
   pip install langchain langchain-openai langchain-community langchain-text-splitters \
               langchain-huggingface langgraph python-dotenv pydantic \
               pypdf pdfplumber docx2txt unstructured faiss-cpu sentence-transformers
   ```

3. 配置环境变量：
   在项目根目录创建 `.env` 文件，添加以下内容：
   ```env
   # 阿里云 DashScope
   OPENAI_API_KEY=your_api_key_here
   BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
   
   # 或 DeepSeek
   API_KEY=your_deepseek_api_key
   ```

### 运行示例

#### Chapter 3 - 记忆与代理

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

#### Chapter 4 - RAG 检索增强生成

进入 chapter4 目录，按顺序学习 RAG 完整流程：
```bash
cd chapter4

# 1. 文档加载基础
python test7.py    # TXT 文档加载
python test8.py    # PDF 文档加载
python test9.py    # Word 文档加载
python test10.py   # Markdown 文档处理

# 2. 批量处理与拆分
python test11.py   # 批量文档加载
python test12.py   # 文本拆分器配置

# 3. 向量库构建与检索
python test13.py   # 向量库构建与检索
python test14.py   # FAISS 完整流程（首次运行会下载模型）

# 4. 高级检索与 LCEL 链式调用
python test15_load_faiss.py  # FAISS 加载详解
python test16.py             # 多策略检索对比
python test17.py             # 检索器详细测试
python test18.py             # LCEL RAG 链式调用（完整版）

# 5. 实用工具
python rebuild_faiss.py      # 重建 FAISS 向量库（修改源文本后运行）
python download_model.py     # 下载嵌入模型到本地
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

### chapter4 - RAG 检索增强生成

本章演示如何构建完整的 RAG（Retrieval-Augmented Generation）系统。

#### test7.py - TXT 文档加载

演示基础的文本加载：
- 使用 TextLoader 加载 .txt 文件
- 理解 Document 对象的结构（page_content + metadata）
- 编码设置避免中文乱码

**关键点**：
- `encoding="utf-8"` 确保中文字符正确读取
- `loader.load()` 返回 `List[Document]`

#### test8.py - PDF 文档加载

演示两种 PDF 加载策略：
- **PyPDFLoader**：轻量级，按页拆分，适合纯文本 PDF
- **PDFPlumberLoader**：重量级，保留表格和格式，适合复杂排版

**关键点**：
- `load_and_split()` 自动按页拆分
- 根据文档类型选择合适的加载器

#### test9.py - Word 文档加载

演示 Word 文档处理：
- 使用 Docx2txtLoader 加载 .docx 文件
- 统一的 Document 接口设计
- 与其他格式保持一致的处理流程

#### test10.py - 批量文档加载

演示工程化的批量处理：
- 遍历文件夹自动识别文件格式（.txt, .pdf, .docx, .md）
- 根据后缀动态选择加载器
- 异常隔离：单个文件失败不影响整体

**关键点**：
- 使用 `os.listdir()` 遍历目录
- `try-except` 确保故障隔离
- `list.extend()` 合并多个文档列表

#### test11.py - 文本拆分器配置

深入讲解 RecursiveCharacterTextSplitter：
- `chunk_size=300`：每个片段的最大字符数
- `chunk_overlap=50`：重叠部分防止语义割裂
- `separators`：中文分隔符优先级（段落 > 句子 > 标点）

**关键点**：
- 递归拆分策略：先按大分隔符切，再按小分隔符切
- 中文需要自定义 separators（`。`, `！`, `？`等）

#### test12.py - Markdown 文档处理

演示结构化文档处理：
- UnstructuredMarkdownLoader 保留标题层级
- MarkdownTextSplitter 智能识别标题边界
- 元数据中包含结构信息

**关键点**：
- `mode="elements"` 启用结构化解析
- 标题作为自然的语义边界

#### test13.py & test14.py - 向量库构建与检索

完整的 RAG 流程演示：
1. **文档加载**：TextLoader 加载文本
2. **文本拆分**：RecursiveCharacterTextSplitter 切分
3. **向量化**：HuggingFaceEmbeddings 生成向量
4. **存储**：FAISS 向量库持久化到本地
5. **检索**：similarity_search_with_score 相似性搜索

**关键点**：
- 使用 BAAI/bge-small-zh-v1.5 中文嵌入模型
- `device="cpu"` 无需 GPU 即可运行
- `normalize_embeddings=True` 提升检索精度
- FAISS 索引可保存和重新加载

## 📚 学习笔记

### 记忆管理（Chapter 3）

- **全量记忆**：保留所有历史消息，适合需要记住所有信息的场景
- **窗口记忆**：只保留最近 N 轮对话，节省 token 成本
- **摘要记忆**：通过压缩历史为摘要，平衡记忆完整性和 token 消耗

### Agent 应用（Chapter 3）

- **工具定义**：使用 `@tool` 装饰器快速创建工具
- **参数验证**：使用 Pydantic 定义参数模型，确保类型安全
- **工具集成**：支持多种工具组合，实现复杂任务

### RAG 检索增强生成（Chapter 4）

**核心流程**：
1. **文档加载（Loading）**：从各种格式（TXT/PDF/Word/MD）提取文本
2. **文本拆分（Splitting）**：将长文档切分为小块，保持语义完整
3. **向量化（Embedding）**：使用嵌入模型将文本转为向量
4. **存储（Storage）**：将向量存入向量数据库（FAISS）
5. **检索（Retrieval）**：根据用户查询找到最相关的文本片段
6. **生成（Generation）**：LLM 基于检索到的内容生成回答

**关键技术点**：
- **统一接口**：所有加载器返回 `List[Document]`，便于后续处理
- **递归拆分**：优先在大边界（段落、句子）处切分
- **向量相似度**：使用余弦相似度衡量文本相关性
- **本地部署**：CPU 即可运行，无需昂贵 GPU

### 核心概念

- LangChain 是一个用于构建语言模型应用的框架
- 提供了各种工具和组件，方便构建复杂的应用
- 支持多种语言模型和工具集成
- 核心组件包括：模型、提示词模板、记忆管理、工具、Agent、RAG 等

## 📝 注意事项

### 通用配置

1. 确保正确配置 `.env` 文件中的 API Key
2. 根据实际使用的模型调整 `model` 参数（如 qwen-plus、qwen-turbo、deepseek-chat 等）
3. 注意 API 调用的费用限制，合理使用记忆策略
4. 合理设置 `temperature` 参数，控制输出的随机性
5. 生产环境中建议使用数据库存储会话历史，而非内存存储

### RAG 相关

6. **首次运行慢**：第一次运行 RAG 示例时，会自动下载 Embedding 模型（约 100MB），请耐心等待
7. **路径问题**：如遇到 `FileNotFoundError`，请检查 `knowledge_base` 文件夹是否在正确位置
8. **代理问题**：如遇到 SSL 错误，请关闭系统代理或使用 `--trusted-host` 参数
9. **CPU vs GPU**：示例默认使用 CPU，如有 NVIDIA 显卡可改为 `"device": "cuda"` 加速
10. **中文优化**：使用 BAAI/bge-small-zh-v1.5 等针对中文优化的嵌入模型
