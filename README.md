# LangChain 和 LangGraph 学习项目

这个项目是我学习 LangChain 和 LangGraph 的代码集合和笔记。

## 目录结构

```
langent-env/
├── langchain/                    # LangChain 学习示例
│   ├── README.md                 # LangChain 学习说明
│   ├── test1.py                  # 基础模型调用示例
│   ├── test2.py                  # 系统提示词设置示例
│   ├── test3.py                  # 多轮对话示例
│   ├── test4.py                  # PromptTemplate 使用示例
│   ├── test5.py                  # FewShotPromptTemplate 使用示例
│   ├── test6.py                  # 自定义 ExampleSelector 示例
│   ├── test7.py                  # 输出解析器 (StrOutputParser) 示例
│   └── learning_method_example.json # 学习方法示例数据
├── langgraph/                    # LangGraph 学习示例
│   ├── README.md                 # LangGraph 学习说明
│   └── test1.py                  # LangGraph 基础示例
├── .gitignore                    # Git 忽略文件
├── README.md                     # 项目说明（本文件）
├── requirements.txt              # 依赖列表
└── run.py                        # 运行脚本
```

## 文件说明

### LangChain 目录

`langchain/` 目录包含 LangChain 学习示例和笔记：

- [查看 LangChain 学习说明](langchain/README.md)

**文件列表**：
- `test1.py`: 基础模型调用示例
  - 演示如何使用 LangChain 封装大语言模型进行基础对话
  - 使用 ChatOpenAI 封装模型，设置模型参数
  - 通过 invoke() 方法调用模型

- `test2.py`: 系统提示词设置示例
  - 展示如何设置系统提示词来定义 AI 的角色和行为
  - 构造多角色消息列表
  - 实现角色化的对话回复

- `test3.py`: 多轮对话示例
  - 演示如何实现多轮对话功能
  - 维护对话历史记录
  - 实现上下文关联的连续对话

- `test4.py`: PromptTemplate 使用示例
  - 展示如何使用提示词模板
  - 定义动态提示词模板
  - 使用 input_variables 设置参数

- `test5.py`: FewShotPromptTemplate 使用示例
  - 演示少样本提示（Few-Shot Prompting）技术
  - 定义示例数据
  - 使用 FewShotPromptTemplate 生成提示词

- `test6.py`: 自定义 ExampleSelector 示例
  - 展示如何自定义示例选择器
  - 继承 BaseExampleSelector 类
  - 实现动态示例选择逻辑

- `test7.py`: 输出解析器示例
  - 演示如何使用输出解析器
  - 使用 StrOutputParser 解析模型输出
  - 构建模型→解析器的链

### LangGraph 目录

`langgraph/` 目录包含 LangGraph 学习示例和笔记：

- [查看 LangGraph 学习说明](langgraph/README.md)

**文件列表**：
- `test1.py`: LangGraph 基础示例
  - 演示如何构建简单的工作流
  - 展示图结构的工作流
  - 支持状态管理和节点之间的数据流

### 项目文件

- `requirements.txt`: 项目依赖列表
- `run.py`: 便捷运行脚本，可以运行所有示例或特定示例
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

您可以使用以下两种方式运行示例：

### 使用 run.py 脚本（推荐）

运行所有示例：
```bash
python run.py all
```

运行特定示例：
```bash
python run.py langchain    # 运行 LangChain 示例
python run.py langgraph    # 运行 LangGraph 示例
```

### 直接运行

运行 LangChain 基础示例：
```bash
cd langchain
python test1.py
```

运行 LangGraph 基础示例：
```bash
cd langgraph
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