
# 多行导入，使用圆括号()讲多个导入项换行排列
# Langchain将它们统一在document_loaders模块中统一导出，因此可以直接导入
# 体现适配器模式
from langchain_community.document_loaders import (
    TextLoader, PyPDFLoader, Docx2txtLoader, UnstructuredMarkdownLoader
)
import os

def batch_load_documents(folder_path):
    # 标准注释
    """
    批量加载文件夹内的所有官方支持格式文档（基于新版加载器）
    :param folder_path: 知识库文件夹路径
    :return: 所有文档的Document对象列表
    """
    all_docs = [] # 存储所有文档的列表
    # 遍历文件夹内所有文件
    # os.listdir()返回指定路径下的所有文件和文件名称列表
    for filename in os.listdir(folder_path):
        # os.path.join() 确保在不同操作系统下路径拼接正确
        file_path = os.path.join(folder_path, filename)
        # 跳过文件夹，只处理文件
        if os.path.isdir(file_path):
            continue
        # 根据文件后缀选择对应的官方推荐加载器
        try:
            if filename.endswith(".txt"):
                loader = TextLoader(file_path, encoding="utf-8")
            elif filename.endswith(".pdf"):
                loader = PyPDFLoader(file_path)  # 基础款，复杂场景可替换为PDFPlumberLoader
            elif filename.endswith(".docx"):
                loader = Docx2txtLoader(file_path)
            elif filename.endswith(".md"):
                loader = UnstructuredMarkdownLoader(file_path)
            else:
                print(f"不支持的文件格式：{filename}")
                continue
            # 加载并添加到文档列表
            docs = loader.load()
            # all_docs为一个大列表，docs是每个加载器返回的小列表List[Document]
            # 如果使用append，那么会变成嵌套列表[[doc1],[doc2]],而不是平铺的[doc1,doc2]
            all_docs.extend(docs)
            print(f"成功加载：{filename}，生成{len(docs)}个Document对象")
        except Exception as e:
            print(f"加载失败：{filename}，错误信息：{str(e)}")
    return all_docs

# 测试批量加载
if __name__ == "__main__":
    knowledge_base_path = "knowledge_base"
    # 确保知识库文件夹存在
    if not os.path.exists(knowledge_base_path):
        # 创建文件夹
        os.makedirs(knowledge_base_path)
        print(f"已自动创建知识库文件夹：{knowledge_base_path}，请放入测试文档")
    else:
        all_docs = batch_load_documents(knowledge_base_path)
        print(f"\n批量加载完成，总Document对象数：{len(all_docs)}")
        # 打印每个文档的基本信息
        # enumerate()函数返回一个索引值和元素组成的元组
        # 同时获取索引1和元素doc
        # doc.metadata是一个字典，包含文档的元数据
        for i, doc in enumerate(all_docs):
            print(f"\n文档{i+1}：")
            print(f"内容预览：{doc.page_content[:100]}...")
            print(f"元数据：{doc.metadata}")