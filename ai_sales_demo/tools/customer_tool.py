import json


class CustomerTool:
    """
    客户信息查询工具。

    负责从 customers.json 中查询客户基础信息。
    """

    def __init__(self, data_path="data/customers.json"):
        self.data_path = data_path

        # 启动时加载客户数据
        with open(
            self.data_path,
            "r",
            encoding="utf-8"
        ) as f:
            self.customers = json.load(f)

    def get_customer(self, customer_id):
        """
        根据 customer_id 查询客户。

        参数：
            customer_id: 客户ID，例如 C10001

        返回：
            客户信息字典
        """

        for customer in self.customers:

            if customer["customer_id"] == customer_id:
                return customer

        return None