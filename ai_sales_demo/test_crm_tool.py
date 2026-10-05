from tools.crm_tool import CRMTool


def main():

    crm_tool = CRMTool()

    print("=" * 60)
    print("CRM Tool 测试")
    print("=" * 60)

    # ========================================================
    # 1. 查询 CRM
    # ========================================================

    customer_id = "C10001"

    customer = crm_tool.get_customer_crm(customer_id)

    print("\n查询客户 CRM：", customer_id)
    print("查询结果：")
    print(customer)

    # ========================================================
    # 2. 更新 CRM
    # ========================================================

    print("\n" + "=" * 60)
    print("更新 CRM")
    print("=" * 60)

    updated_customer = crm_tool.update_customer(
        customer_id="C10001",
        intent_level="高",
        follow_up_status="重点跟进",
        last_result="客户明确表示对信用卡感兴趣",
        next_action="跟进申请流程"
    )

    print("\n更新后的 CRM：")
    print(updated_customer)

    # ========================================================
    # 3. 再次读取，确认真的写入文件
    # ========================================================

    print("\n" + "=" * 60)
    print("重新读取 CRM")
    print("=" * 60)

    new_crm_tool = CRMTool()

    customer = new_crm_tool.get_customer_crm("C10001")

    print("\n重新读取结果：")
    print(customer)


if __name__ == "__main__":
    main()