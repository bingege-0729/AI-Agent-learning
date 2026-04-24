"""
模型下载脚本 - 使用 HuggingFace 国内镜像源
用法: python download_model.py
"""
import os

# 必须在导入 huggingface_hub 之前设置环境变量
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'
os.environ['HF_HUB_DOWNLOAD_TIMEOUT'] = '300'  # 5分钟超时

from huggingface_hub import snapshot_download

# ==================== 配置区域 ====================
# 选择要下载的模型（取消注释其中一个）

# 选项1: BAAI/bge-small-zh-v1.5 (推荐，约200MB)
model_id = "BAAI/bge-small-zh-v1.5"
local_dir = "./models/BAAI/bge-small-zh-v1.5"

# 选项2: Qwen/Qwen3-Embedding-0.6B (较大，约1GB+)
# model_id = "Qwen/Qwen3-Embedding-0.6B"
# local_dir = "./models/Qwen/Qwen3-Embedding-0___6B"

# ================================================

print(f"开始下载模型: {model_id}")
print(f"保存路径: {local_dir}")
print("首次下载可能需要几分钟，请耐心等待...\n")

try:
    snapshot_download(
        repo_id=model_id,           # 模型仓库ID
        local_dir=local_dir,        # 本地保存路径
        local_dir_use_symlinks=False,  # 不使用符号链接（Windows兼容）
        resume_download=True,       # 支持断点续传
    )
    print(f"\n✓ 模型下载成功！")
    print(f"  位置: {os.path.abspath(local_dir)}")
    print(f"\n在代码中使用:")
    print(f'  embedding_model_name = "{local_dir}"')
except Exception as e:
    print(f"\n✗ 下载失败: {str(e)}")
    print("\n如果仍然超时，请尝试:")
    print("1. 检查网络连接")
    print("2. 使用方案2：手动从浏览器下载")
    print("3. 使用命令行工具 huggingface-cli")
