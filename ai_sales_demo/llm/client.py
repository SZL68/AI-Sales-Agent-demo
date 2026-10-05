"""
LLM Client

负责：
1. 初始化 LLM Client
2. 调用大语言模型
3. 对上层 Agent 屏蔽具体模型 API 细节
"""

from openai import OpenAI

from config import API_KEY, BASE_URL, MODEL


class LLMClient:

    def __init__(self):
        if not API_KEY:
            raise ValueError(
                "没有找到 OPENAI_API_KEY，请检查 .env 文件。"
            )

        self.client = OpenAI(
            api_key=API_KEY,
            base_url=BASE_URL
        )

        self.model = MODEL

    def chat(
        self,
        messages,
        temperature=0.3
    ):
        """
        普通对话调用
        """

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature
        )

        return response.choices[0].message.content