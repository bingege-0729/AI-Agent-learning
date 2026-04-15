# LangChain 学习示例

这个目录包含了我学习 LangChain 的示例代码和笔记。

## 📁 目录结构

```
langchain/
├── test1.py                    # 基础模型调用示例
├── test2.py                    # 系统提示词设置示例
├── test3.py                    # 多轮对话示例
├── test4.py                    # PromptTemplate 使用示例
├── test5.py                    # FewShotPromptTemplate 使用示例
├── test6.py                    # 自定义 ExampleSelector 示例
├── test7.py                    # 输出解析器 (StrOutputParser) 示例
└── learning_method_example.json # 学习方法示例数据
```

## 🚀 快速开始

### 环境准备

1. 确保已安装 Python 3.8+
2. 安装必要的依赖包：
   ```bash
   pip install langchain langchain-openai langchain-community python-dotenv
   ```

3. 配置环境变量：
   在项目根目录创建 `.env` 文件，添加以下内容：
   ```env
   OPENAI_API_KEY=your_api_key_here
   BASE_URL=your_base_url_here
   ```

### 运行示例

每个测试文件都可以独立运行：
```bash
python test1.py
```

## 📖 文件说明

### test1.py - 基础模型调用

演示如何使用 LangChain 封装大语言模型进行基础对话：
- 初始化 ChatOpenAI 模型
- 设置模型参数（temperature、max_tokens 等）
- 调用 invoke 方法生成回复

**关键点**：
- 使用 `ChatOpenAI` 封装模型，无需手动编写 HTTP 请求
- 通过 `invoke()` 方法调用模型
- 结果通过 `response.content` 获取

### test2.py - 系统提示词设置

展示如何设置系统提示词来定义 AI 的角色和行为：
- 定义 system 角色提示词
- 构造多角色消息列表
- 实现角色化的对话回复

**关键点**：
- 使用消息列表格式：`[{"role": "system", "content": "..."}]`
- system 角色用于设定 AI 的行为准则
- user 角色用于发送用户请求

### test3.py - 多轮对话

演示如何实现多轮对话功能：
- 维护对话历史记录
- 实现上下文关联的连续对话
- 支持追问和多轮交互

**关键点**：
- 使用列表维护对话历史
- 每次对话后更新历史记录
- 将历史记录作为上下文传递给模型

### test4.py - PromptTemplate 使用

展示如何使用提示词模板：
- 定义动态提示词模板
- 使用 input_variables 设置参数
- 通过 format 方法填充模板

**关键点**：
- `PromptTemplate` 用于创建可复用的提示词模板
- 使用 `{参数名}` 定义占位符
- 通过 `format()` 方法填充实际参数

### test5.py - FewShotPromptTemplate 使用

演示少样本提示（Few-Shot Prompting）技术：
- 定义示例数据
- 创建示例模板
- 使用 FewShotPromptTemplate 生成提示词

**关键点**：
- 少样本提示通过提供示例帮助模型理解任务
- `FewShotPromptTemplate` 结合示例和用户输入
- 示例数据可以来自 JSON 文件或代码中定义

### test6.py - 自定义 ExampleSelector

展示如何自定义示例选择器：
- 继承 `BaseExampleSelector` 类
- 实现动态示例选择逻辑
- 根据难度等级筛选示例

**关键点**：
- 自定义 `ExampleSelector` 可根据输入特征选择示例
- 实现 `select_examples` 方法定义选择逻辑
- 支持多种选择策略（按长度、难度等）

### test7.py - 输出解析器

演示如何使用输出解析器：
- 使用 `StrOutputParser` 解析模型输出
- 构建模型→解析器的链
- 获取字符串格式的输出结果

**关键点**：
- `StrOutputParser` 将 AIMessage 转换为字符串
- 使用 `|` 操作符构建链
- 输出解析器简化结果处理流程

## 📚 学习笔记

- LangChain 是一个用于构建语言模型应用的框架
- 提供了各种工具和组件，方便构建复杂的应用
- 支持多种语言模型和工具集成
- 核心组件包括：模型、提示词模板、输出解析器、链等

## 📝 注意事项

1. 确保正确配置 `.env` 文件中的 API Key
2. 根据实际使用的模型调整 `model` 参数
3. 注意 API 调用的费用限制
4. 合理设置 `temperature` 和 `max_tokens` 参数
