from tools.customer_tool import CustomerTool


def main():

    customer_tool = CustomerTool()

    print("=" * 60)
    print("Customer Tool 测试")
    print("=" * 60)

    # 测试存在的客户
    customer_id = "C10001"

    customer = customer_tool.get_customer(customer_id)

    print("\n查询客户：", customer_id)
    print("查询结果：")
    print(customer)

    # 测试不存在的客户
    customer_id = "C99999"

    customer = customer_tool.get_customer(customer_id)

    print("\n查询客户：", customer_id)
    print("查询结果：")
    print(customer)


if __name__ == "__main__":
    main()