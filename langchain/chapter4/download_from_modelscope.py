"""
使用 ModelScope（阿里镜像）下载模型 - 国内速度最快
用法: python download_from_modelscope.py
"""
from modelscope import snapshot_download

# 选择要下载的模型
# ModelScope 上的模型ID可能与 HuggingFace 不同

# 选项1: BGE small zh v1.5
model_id = "AI-ModelScope/bge-small-zh-v1.5"
cache_dir = "./models/modelscope_cache"

print(f"从 ModelScope 下载模型: {model_id}")
print("这可能需要几分钟...\n")

try:
    model_dir = snapshot_download(
        model_id,
        cache_dir=cache_dir,
        revision='master'
    )
    print(f"\n✓ 下载成功！")
    print(f"模型位置: {model_dir}")
    print(f"\n在代码中使用:")
    print(f'  embedding_model_name = r"{model_dir}"')
except Exception as e:
    print(f"\n✗ 下载失败: {str(e)}")
