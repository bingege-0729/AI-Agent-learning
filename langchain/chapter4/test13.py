from langchain_text_splitters import MarkdownTextSplitter

# MarkdownTextSplitter：专门针对 Markdown 格式优化的拆分器，能识别标题层级
from langchain_community.document_loaders import UnstructuredMarkdownLoader  # 官方推荐MD加载器
from pathlib import Path

# 加载MD文档（保留标题层级元数据）
md_path = Path("knowledge_base") / "test.md"
                                    # 显示类型转换（手动） # 告诉加载器以元素模式解析
                                    # 会尝试保留 Markdown 的结构（如标题、列表、代码块），并在 metadata 中记录这些信息。
loader = UnstructuredMarkdownLoader(str(md_path), mode="elements")  # Path转字符串兼容所有版本
md_docs = loader.load()

# 3. 初始化MD分割器（保留你原有核心参数，1.x版本完全兼容）
text_splitter = MarkdownTextSplitter(
    chunk_size=500,  # MD有标题引导，片段长度可稍大
    chunk_overlap=50,  # 重叠部分避免标题/内容割裂
    length_function=len  # 中文用len计数字符
)

# 4. 执行分割（方法名split_documents在1.x版本无变化）
# 多态性：虽然加载器换成了 UnstructuredMarkdownLoader，
# 拆分器换成了 MarkdownTextSplitter，
# 但调用的方法名依然是 split_documents。

# 输入：List[Document]
# 输出：List[Document]
# 体现Langchain接口的一致性
split_docs = text_splitter.split_documents(md_docs)

# 5. 验证结果（片段会保留MD标题层级，符合预期）
print(f"分割后片段数：{len(split_docs)}")
print("\n前2个MD片段示例：")
for i, doc in enumerate(split_docs[:2]):
    print(f"\n片段{i + 1}：")
    print(doc.page_content.strip())
