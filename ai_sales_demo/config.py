"""
AI 电销系统配置文件
"""

import os
from dotenv import load_dotenv


# 加载 .env
load_dotenv()


# =========================
# LLM 配置
# =========================

API_KEY = os.getenv("OPENAI_API_KEY")

BASE_URL = os.getenv(
    "OPENAI_BASE_URL",
    "https://api.openai.com/v1"
)

MODEL = os.getenv(
    "OPENAI_MODEL",
    "gpt-4o-mini"
)


# =========================
# 项目配置
# =========================

PROJECT_NAME = "AI Sales Demo"

DEFAULT_CUSTOMER_ID = "C10001"