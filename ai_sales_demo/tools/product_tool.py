class ProductTool:
    """
    产品信息查询工具。

    当前使用内存中的模拟产品数据。
    实际生产系统中，这里可以连接数据库或产品管理 API。
    """

    def __init__(self):

        self.products = [
            {
                "product_id": "P001",
                "name": "青春信用卡",
                "annual_fee": 0,
                "estimated_limit": "10000-50000",
                "benefits": [
                    "新户礼",
                    "消费积分",
                    "线上优惠"
                ],
                "application_method": [
                    "线上申请",
                    "APP申请"
                ]
            },
            {
                "product_id": "P002",
                "name": "尊享信用卡",
                "annual_fee": 200,
                "estimated_limit": "50000-200000",
                "benefits": [
                    "高端消费权益",
                    "机场贵宾厅",
                    "积分兑换"
                ],
                "application_method": [
                    "线上申请",
                    "人工审核"
                ]
            }
        ]

    def get_product(self, product_id):
        """
        根据产品ID查询产品信息。
        """

        for product in self.products:

            if product["product_id"] == product_id:
                return product

        return None

    def get_all_products(self):
        """
        获取全部产品。
        """

        return self.products