"""
测试 LLM API 是否能够正常调用。

运行：

    python test_api.py
"""

from llm.client import LLMClient


def main():

    print("=" * 60)
    print("开始测试 LLM API")
    print("=" * 60)

    try:

        # 创建 LLM 客户端
        llm = LLMClient()

        # 构造测试消息
        messages = [
            {
                "role": "system",
                "content": "你是一名专业的AI电销助手。"
            },
            {
                "role": "user",
                "content": "请用一句话介绍你自己。"
            }
        ]

        # 调用 LLM
        result = llm.chat(messages)

        print("\nLLM 返回：")
        print(result)

        print("\n" + "=" * 60)
        print("API 测试成功")
        print("=" * 60)

    except Exception as e:

        print("\n" + "=" * 60)
        print("API 测试失败")
        print("=" * 60)

        print("错误类型：", type(e).__name__)
        print("错误信息：", e)


if __name__ == "__main__":
    main()