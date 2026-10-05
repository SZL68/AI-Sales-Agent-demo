class ConversationState:
    """
    保存一次销售对话过程中的状态。
    """

    def __init__(self, customer_id):
        self.customer_id = customer_id

        # 当前客户信息
        self.customer_info = None

        # 当前 CRM 信息
        self.crm_info = None

        # 当前识别出的客户意图
        self.current_intent = None

        # 当前产品信息
        self.product_info = None

        # 最近一次客户说的话
        self.last_user_message = None

        # AI 最近一次回复
        self.last_assistant_message = None

        # 对话历史
        self.history = []

    def add_message(self, role, content):
        """
        保存一条对话消息。
        """
        self.history.append({
            "role": role,
            "content": content
        })

        if role == "user":
            self.last_user_message = content

        elif role == "assistant":
            self.last_assistant_message = content