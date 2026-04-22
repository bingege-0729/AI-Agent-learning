from langchain_text_splitters import RecursiveCharacterTextSplitter
# 负责文本切分逻辑
from langchain_community.document_loaders import TextLoader  # LangChain推荐的基础文本加载器
from pathlib import Path  # 官方推荐用pathlib处理路径（比os.path更现代）
# 面向对象路径方法
# 1. 加载文档（推荐用Path处理路径，避免跨系统兼容问题）
txt_path = Path("knowledge_base") / "test.txt" # 使用 / 运算符拼接路径
loader = TextLoader(txt_path, encoding="utf-8")
txt_docs = loader.load()  # 返回Document对象列表（含内容+元数据）

# 2. 初始化分割器（LangChain推荐参数）
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,  # 中文片段推荐长度：200-500字
    chunk_overlap=50,  # 重叠长度：建议为chunk_size的10%-20%，避免跨片段语义丢失
    length_function=len,  # 中文用len计数，英文可改用tiktoken.count_tokens
    separators=["\n\n", "\n", "。", "！", "？", "，", "；", "、"]  # 中文推荐分隔符优先级
)
# 分割器尽量保持句子的完整性，避免在单词或短语中间强行切断



# 3. 执行分割（split_documents为官方推荐方法，接收Document列表）
split_docs = text_splitter.split_documents(txt_docs)
# split_documents是TextSplitter的抽象方法，可接受Document对象列表

# 输入：List[Document]（原始文档列表）。
# 输出：List[Document]（拆分后的片段列表）
# 元数据继承：拆分后的每个小片段都会自动复制原始文档的 metadata（如文件路径）。
# 自动追加页码/索引：某些拆分器还会在 metadata 中增加 chunk_index 等信息。

# 4. 验证结果
print(f"原始文档数：{len(txt_docs)}")
print(f"分割后片段数：{len(split_docs)}")
print("\n前3个片段示例：")
for i, doc in enumerate(split_docs[:3]):
    print(f"\n片段{i + 1}（字符数：{len(doc.page_content)}）：")
    print(doc.page_content.strip())# .strip()去除字符串首尾的空白字符
    # len(doc.page_content)：在循环内部实时计算当前片段的实际字符数
    print(f"片段元数据：{doc.metadata}")  # 保留原始文档路径等元数据（检索时有用）
