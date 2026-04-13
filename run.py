#!/usr/bin/env python3
"""
LangChain 和 LangGraph 学习项目运行脚本

使用方法:
    python run.py langchain    # 运行 LangChain 示例
    python run.py langgraph    # 运行 LangGraph 示例
    python run.py all          # 运行所有示例
"""

import os
import sys
import subprocess


def run_langchain_example():
    """运行 LangChain 示例"""
    print("运行 LangChain 示例...")
    os.chdir("langchain")
    subprocess.run([sys.executable, "test1.py"])
    os.chdir("..")


def run_langgraph_example():
    """运行 LangGraph 示例"""
    print("运行 LangGraph 示例...")
    os.chdir("langgraph")
    subprocess.run([sys.executable, "test1.py"])
    os.chdir("..")


def run_all_examples():
    """运行所有示例"""
    run_langchain_example()
    print()
    run_langgraph_example()


def main():
    if len(sys.argv) < 2:
        print("使用方法:")
        print("  python run.py langchain    # 运行 LangChain 示例")
        print("  python run.py langgraph    # 运行 LangGraph 示例")
        print("  python run.py all          # 运行所有示例")
        return

    example = sys.argv[1].lower()

    if example == "langchain":
        run_langchain_example()
    elif example == "langgraph":
        run_langgraph_example()
    elif example == "all":
        run_all_examples()
    else:
        print(f"未知的示例: {example}")
        print("可用的示例: langchain, langgraph, all")


if __name__ == "__main__":
    main()
