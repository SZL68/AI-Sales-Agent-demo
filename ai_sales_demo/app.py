from agent.sales_agent import SalesAgent


def main():

    print("=" * 60)
    print("              AI Sales Demo")
    print("=" * 60)

    # ==========================================
    # 1. 输入客户ID
    # ==========================================

    customer_id = input(
        "\n请输入客户ID（例如 C10001）："
    ).strip()

    # ==========================================
    # 2. 创建销售Agent
    # ==========================================

    try:

        agent = SalesAgent(
            customer_id=customer_id
        )

    except Exception as e:

        print("\nAgent 初始化失败：")
        print(e)

        return

    # ==========================================
    # 3. 检查客户是否存在
    # ==========================================

    if agent.state.customer_info is None:

        print(
            f"\n没有找到客户：{customer_id}"
        )

        return

    customer = agent.state.customer_info

    print("\n客户信息：")
    print(
        f"客户：{customer['name']}"
    )
    print(
        f"城市：{customer['city']}"
    )
    print(
        f"职业：{customer['occupation']}"
    )

    print("\n" + "=" * 60)
    print("开始AI销售对话")
    print("输入 exit 可以结束对话")
    print("=" * 60)

    # ==========================================
    # 4. 多轮对话
    # ==========================================

    while True:

        user_message = input(
            "\n客户："
        ).strip()

        # 空输入
        if not user_message:
            continue

        # 退出
        if user_message.lower() == "exit":

            print("\n对话结束。")

            break

        # ======================================
        # Agent处理
        # ======================================

        try:

            response = agent.process(
                user_message
            )

            print(
                f"\nAI：{response}"
            )

        except Exception as e:

            print("\n处理请求时发生错误：")
            print(e)


if __name__ == "__main__":
    main()