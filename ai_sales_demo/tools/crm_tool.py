import json


class CRMTool:
    """
    CRM 工具。

    负责：
    1. 查询客户跟进信息
    2. 更新客户意向
    3. 更新跟进状态
    4. 记录沟通结果
    """

    def __init__(self, data_path="data/crm.json"):

        self.data_path = data_path

        # 读取 CRM 数据
        with open(
            self.data_path,
            "r",
            encoding="utf-8"
        ) as f:
            self.crm_data = json.load(f)

    def get_customer_crm(self, customer_id):
        """
        查询客户 CRM 信息。
        """

        for customer in self.crm_data:

            if customer["customer_id"] == customer_id:
                return customer

        return None

    def update_customer(
        self,
        customer_id,
        intent_level=None,
        follow_up_status=None,
        last_result=None,
        next_action=None
    ):
        """
        更新客户 CRM 信息。
        """

        for customer in self.crm_data:

            if customer["customer_id"] == customer_id:

                if intent_level is not None:
                    customer["intent_level"] = intent_level

                if follow_up_status is not None:
                    customer["follow_up_status"] = follow_up_status

                if last_result is not None:
                    customer["last_result"] = last_result

                if next_action is not None:
                    customer["next_action"] = next_action

                customer["contact_count"] += 1

                # 保存到 JSON
                with open(
                    self.data_path,
                    "w",
                    encoding="utf-8"
                ) as f:

                    json.dump(
                        self.crm_data,
                        f,
                        ensure_ascii=False,
                        indent=4
                    )

                return customer

        return None