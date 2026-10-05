from tools.product_tool import ProductTool


def main():

    product_tool = ProductTool()

    print("=" * 60)
    print("Product Tool 测试")
    print("=" * 60)

    # 测试查询产品
    product_id = "P001"

    product = product_tool.get_product(product_id)

    print("\n查询产品：", product_id)
    print("查询结果：")
    print(product)

    # 测试查询全部产品
    print("\n" + "=" * 60)
    print("全部产品")
    print("=" * 60)

    products = product_tool.get_all_products()

    for product in products:
        print(
            f"\n产品ID：{product['product_id']}"
            f"\n产品名称：{product['name']}"
            f"\n年费：{product['annual_fee']}"
            f"\n额度范围：{product['estimated_limit']}"
        )

    # 测试不存在的产品
    product_id = "P999"

    product = product_tool.get_product(product_id)

    print("\n" + "=" * 60)
    print("测试不存在的产品")
    print("=" * 60)

    print("查询产品：", product_id)
    print("查询结果：", product)


if __name__ == "__main__":
    main()