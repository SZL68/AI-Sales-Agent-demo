from agent.sales_agent import SalesAgent


def main():

    print("=" * 60)
    print("SalesAgent 多轮对话测试")
    print("=" * 60)

    # 创建一个客户对应的 Agent
    agent = SalesAgent(
        customer_id="C10001"
    )

    # 模拟真实销售对话
    conversation = [
        "这张卡有什么优惠？",
        "那额度大概是多少？",
        "听起来不错，我想申请。",
        "那就现在帮我办理吧。"
    ]

    for i, user_message in enumerate(conversation, start=1):

        print("\n")
        print("#" * 60)
        print(f"第 {i} 轮对话")
        print("#" * 60)

        print(f"\n客户：{user_message}")

        response = agent.process(
            user_message
        )

        print(f"\nAI：{response}")

        print("\n当前客户状态：")
        print(f"客户意图：{agent.state.current_intent}")
        print(f"CRM信息：{agent.state.crm_info}")

        print("\n当前对话历史：")
        for message in agent.state.history:
            print(
                f"{message['role']}："
                f"{message['content']}"
            )


if __name__ == "__main__":
    main()