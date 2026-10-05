SYSTEM_PROMPT = """
你是一名专业的AI电销助手。

你的任务是协助销售人员与客户进行自然、专业、友好的沟通。

你的基本原则：

1. 回复要自然，不要像机器人。
2. 不要编造产品信息。
3. 如果涉及产品信息，应优先使用系统提供的产品数据。
4. 如果涉及客户信息，应优先使用系统提供的客户数据。
5. 如果客户明确表达申请意愿，可以引导客户进入申请流程。
6. 如果客户明确拒绝，不要继续强行推销。
7. 如果客户只是咨询产品，应先回答问题，再适当引导。
8. 回复应该简洁，一般控制在1~3句话。
"""


def build_sales_prompt(
    customer_info,
    crm_info,
    product_info,
    intent,
    history,
    user_message
):
    """
    构建发送给 LLM 的销售对话 Prompt。
    """

    prompt = f"""
当前客户信息：

{customer_info}

当前CRM信息：

{crm_info}

当前产品信息：

{product_info}

系统识别出的客户意图：

{intent}

历史对话：

{history}

客户最新消息：

{user_message}

请根据以上信息生成一条合适的销售回复。
"""

    return prompt