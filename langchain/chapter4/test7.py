# 导入TXT加载器（新版路径：langchain_community.document_loaders）
from langchain_community.document_loaders import TextLoader
import os # 操作系统相关功能

# 定义文档路径（请替换成你自己的路径）
# join调用，拼接路径
# knowledge_base为文档所在目录，test.txt为文档名称
# 可以传入多个参数：os.path.join("a", "b", "c.txt") → "a/b/c.txt"
# windows 系统下，路径分隔符为\，需要使用os.path.join()函数拼接路径
txt_path = os.path.join("knowledge_base", "test.txt")

# 初始化加载器并加载文档
# TextLoader()调用类的构造函数（__init__方法）
# 创建TextLoader对象
loader = TextLoader(txt_path, encoding="utf-8")  # 指定编码，避免中文乱码
txt_docs = loader.load()  # load()返回Document对象列表（即使只有一个文档）


# txt_docs的结构
# txt_docs = [
#     Document(
#         page_content="文件的完整文本内容...",
#         metadata={"source": "knowledge_base/test.txt"}
#     )
# ]
# 查看加载结果
print("TXT文档加载结果：")
print(f"文档数量：{len(txt_docs)}")
print(f"文档内容：{txt_docs[0].page_content[:200]}...")  # 打印前200个字符
print(f"文档元数据：{txt_docs[0].metadata}")  # 元数据包含文档路径等信息