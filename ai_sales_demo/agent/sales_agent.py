from services.intent import IntentClassifier
from tools.customer_tool import CustomerTool
from tools.product_tool import ProductTool
from tools.crm_tool import CRMTool

from agent.state import ConversationState
from agent.prompt import build_sales_prompt

from llm.client import LLMClient


class SalesAgent:
    """
    AI销售Agent。

    负责协调：
    - 意图识别
    - 客户信息查询
    - 产品信息查询
    - CRM操作
    - LLM回复
    """

    def __init__(self, customer_id):

        # ==========================================
        # 1. 初始化各种业务模块
        # ==========================================

        self.intent_classifier = IntentClassifier()

        self.customer_tool = CustomerTool()

        self.product_tool = ProductTool()

        self.crm_tool = CRMTool()

        self.llm = LLMClient()

        # ==========================================
        # 2. 初始化对话状态
        # ==========================================

        self.state = ConversationState(customer_id)

        # 查询客户信息
        self.state.customer_info = (
            self.customer_tool.get_customer(customer_id)
        )

        # 查询 CRM 信息
        self.state.crm_info = (
            self.crm_tool.get_customer_crm(customer_id)
        )

    def update_crm_by_intent(self, intent, user_message):
        """
        根据客户当前意图，自动更新 CRM。

        注意：
        这里是业务规则，不交给 LLM 自由决定。
        """

        customer_id = self.state.customer_id

        # ==========================================
        # 高意向
        # ==========================================

        if intent == "高意向":

            updated_crm = self.crm_tool.update_customer(
                customer_id=customer_id,
                intent_level="高",
                follow_up_status="重点跟进",
                last_result=f"客户明确表达高意向：{user_message}",
                next_action="跟进申请流程"
            )

            print("\n[CRM] 客户被标记为高意向")
            print("[CRM] 跟进状态：重点跟进")

        # ==========================================
        # 申请意向
        # ==========================================

        elif intent == "申请意向":

            updated_crm = self.crm_tool.update_customer(
                customer_id=customer_id,
                intent_level="中",
                follow_up_status="待跟进",
                last_result=f"客户表达申请意向：{user_message}",
                next_action="进一步介绍申请条件和流程"
            )

            print("\n[CRM] 客户被标记为申请意向")
            print("[CRM] 跟进状态：待跟进")

        # ==========================================
        # 拒绝
        # ==========================================

        elif intent == "拒绝":

            updated_crm = self.crm_tool.update_customer(
                customer_id=customer_id,
                intent_level="低",
                follow_up_status="暂不跟进",
                last_result=f"客户明确拒绝：{user_message}",
                next_action="暂不联系"
            )

            print("\n[CRM] 客户被标记为低意向")
            print("[CRM] 跟进状态：暂不跟进")

        # ==========================================
        # 产品咨询
        # ==========================================

        elif intent == "产品咨询":

            updated_crm = self.crm_tool.update_customer(
                customer_id=customer_id,
                last_result=f"客户咨询产品信息：{user_message}",
                next_action="继续了解客户需求"
            )

            print("\n[CRM] 已记录客户产品咨询")
            print("[CRM] 暂不改变客户意向等级")

        # ==========================================
        # 额度咨询
        # ==========================================

        elif intent == "额度咨询":

            updated_crm = self.crm_tool.update_customer(
                customer_id=customer_id,
                last_result=f"客户咨询额度：{user_message}",
                next_action="介绍额度相关信息"
            )

            print("\n[CRM] 已记录客户额度咨询")

        # ==========================================
        # 费用咨询
        # ==========================================

        elif intent == "费用咨询":

            updated_crm = self.crm_tool.update_customer(
                customer_id=customer_id,
                last_result=f"客户咨询费用：{user_message}",
                next_action="介绍产品费用信息"
            )

            print("\n[CRM] 已记录客户费用咨询")

        else:

            updated_crm = None

            print("\n[CRM] 当前意图无需更新 CRM")

        # ==========================================
        # 更新 Agent 当前状态
        # ==========================================

        if updated_crm is not None:
            self.state.crm_info = updated_crm

        return updated_crm

    def process(self, user_message):

        print("\n" + "=" * 60)
        print("SalesAgent 开始处理")
        print("=" * 60)

        # ==========================================
        # 1. 保存用户消息
        # ==========================================

        self.state.add_message(
            "user",
            user_message
        )

        print("\n[1] 客户消息")
        print(user_message)

        # ==========================================
        # 2. 意图识别
        # ==========================================

        intent = self.intent_classifier.predict(
            user_message
        )

        self.state.current_intent = intent

        print("\n[2] 意图识别")
        print(intent)

        # ==========================================
        # 3. 根据意图调用业务工具
        # ==========================================

        if intent in ["产品咨询", "申请意向", "高意向"]:

            products = self.product_tool.get_all_products()

            self.state.product_info = products

            print("\n[3] 查询产品信息")
            print(products)

        elif intent == "拒绝":

            print("\n[3] 客户拒绝")
            print("停止继续营销")

        else:

            print("\n[3] 当前无需查询全部产品")

        # ==========================================
        # 4. 自动更新 CRM
        # ==========================================

        print("\n[4] 更新 CRM")

        self.update_crm_by_intent(
            intent=intent,
            user_message=user_message
        )

        # ==========================================
        # 5. 构建 Prompt
        # ==========================================

        prompt = build_sales_prompt(
            customer_info=self.state.customer_info,
            crm_info=self.state.crm_info,
            product_info=self.state.product_info,
            intent=self.state.current_intent,
            history=self.state.history,
            user_message=user_message
        )

        print("\n[5] Prompt 已生成")

        # ==========================================
        # 6. 调用 LLM
        # ==========================================

        messages = [
            {
                "role": "system",
                "content": """
你是一名专业的AI电销助手。

请根据客户信息、CRM信息、产品信息和客户意图，
生成自然、专业、简洁的销售回复。

要求：

1. 不要编造系统没有提供的信息。
2. 产品信息必须以系统提供的数据为准。
3. 如果客户明确拒绝，不要继续强行推销。
4. 回复自然，不要暴露内部系统信息。
5. 一般控制在1~3句话。
"""
            },
            {
                "role": "user",
                "content": prompt
            }
        ]

        print("\n[6] 调用 LLM")

        response = self.llm.chat(messages)

        # ==========================================
        # 7. 保存 AI 回复
        # ==========================================

        self.state.add_message(
            "assistant",
            response
        )

        print("\n[7] LLM 回复")
        print(response)

        return response