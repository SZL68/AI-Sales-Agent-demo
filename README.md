# AI Sales Agent

一个基于 **LLM + Agent + Tool + CRM** 构建的 AI 电销助手 Demo。

本项目模拟信用卡销售场景，实现客户信息查询、信用卡产品查询、客户意图识别、CRM 状态管理以及多轮销售对话。

项目重点实践：

* LLM API 调用
* Prompt Engineering
* Agent 架构
* Tool 调用
* 客户意图识别
* CRM 数据管理
* 多轮对话状态管理
* AI 应用业务流程设计

> 本项目主要用于 AI Engineer / LLM Application 的学习与实践，不属于生产级电销系统。

---

## 1. 项目简介

传统的电销系统通常按照固定业务流程处理客户消息：

```text
客户消息
   ↓
意图识别
   ↓
业务逻辑判断
   ↓
调用对应业务工具
   ↓
获取业务数据
   ↓
构建 Prompt
   ↓
LLM
   ↓
生成销售回复
   ↓
更新 CRM
```

本项目按照这一思路构建了一个简单的 AI 电销 Agent。

Agent 可以根据客户当前消息识别客户意图，并根据不同意图调用不同的业务 Tool。

例如：

```text
客户：你们有哪些信用卡？
              ↓
        意图：产品咨询
              ↓
        ProductTool
              ↓
        查询产品信息
              ↓
             LLM
              ↓
        生成销售回复
```

---

# 2. 系统整体架构

```text
                    客户
                     │
                     ↓
               客户自然语言
                     │
                     ↓
              ┌─────────────┐
              │  SalesAgent │
              └──────┬──────┘
                     │
                     ↓
              意图识别模型
                     │
        ┌────────────┼────────────┐
        ↓            ↓            ↓
    产品咨询      申请意向       拒绝
        │            │            │
        └────────────┼────────────┘
                     ↓
              业务 Tool 调用
                     │
        ┌────────────┼────────────┐
        ↓            ↓            ↓
 CustomerTool   ProductTool    CRMTool
        │            │            │
        ↓            ↓            ↓
   客户信息       产品信息       CRM信息
        │            │            │
        └────────────┼────────────┘
                     ↓
              构建销售 Prompt
                     │
                     ↓
                    LLM
                     │
                     ↓
                销售回复
                     │
                     ↓
                更新 CRM
                     │
                     ↓
                下一轮对话
```

---

# 3. 核心功能

## 3.1 客户意图识别

项目使用：

```text
TF-IDF
+
Logistic Regression
```

对客户消息进行意图分类。

目前包含 6 类客户意图：

| 意图   | 示例        |
| ---- | --------- |
| 产品咨询 | 有哪些信用卡？   |
| 额度咨询 | 这张卡额度是多少？ |
| 费用咨询 | 年费是多少？    |
| 申请意向 | 我想申请一张    |
| 拒绝   | 暂时不需要     |
| 高意向  | 那就现在帮我办理吧 |

训练数据共 **48 条**，每类 8 条。

数据划分：

```text
总数据：48
训练集：38
测试集：10
```

测试集 Accuracy：

```text
0.8000
```

由于数据规模较小，该结果主要用于 Demo 验证，不代表生产环境模型性能。

---

# 4. Agent

项目中的 `SalesAgent` 是整个系统的核心控制模块。

它负责协调：

```text
用户输入
    ↓
意图识别
    ↓
业务 Tool
    ↓
Prompt
    ↓
LLM
    ↓
CRM
    ↓
对话状态
```

可以将当前 Agent 理解为：

```text
Agent
=
意图识别
+
业务工具
+
Prompt
+
LLM
+
状态管理
```

---

# 5. Tools

项目将不同业务能力拆分成独立 Tool。

## CustomerTool

负责查询客户基础信息。

数据来源：

```text
data/customers.json
```

可以获取：

```text
客户ID
姓名
年龄
城市
职业
收入水平
历史行为
当前产品
```

例如：

```json
{
    "customer_id": "C10001",
    "name": "张先生",
    "age": 28,
    "city": "上海",
    "occupation": "互联网从业者",
    "income_level": "中等"
}
```

---

## ProductTool

负责查询信用卡产品信息。

当前模拟两个产品：

```text
P001 青春信用卡
P002 尊享信用卡
```

产品信息包括：

```text
产品名称
年费
预计额度
产品权益
申请方式
```

例如：

```text
青春信用卡

年费：0
预计额度：10000-50000
权益：
- 新户礼
- 消费积分
- 线上优惠
```

目前产品数据使用 Python 内存中的模拟数据。

实际生产环境可以替换成：

```text
ProductTool
     ↓
数据库 / 产品 API
```

---

## CRMTool

负责客户销售过程管理。

主要功能：

```text
查询客户 CRM
更新客户意向
更新跟进状态
记录沟通结果
设置下一步行动
统计联系次数
```

CRM 数据目前保存在：

```text
data/crm.json
```

例如：

```json
{
    "customer_id": "C10001",
    "intent_level": "高",
    "follow_up_status": "重点跟进",
    "contact_count": 7,
    "last_result": "客户明确表达高意向",
    "next_action": "跟进申请流程"
}
```

在真实企业系统中，这一层可以进一步连接：

```text
CRMTool
   ↓
CRM API
   ↓
企业 CRM 系统
```

---

# 6. LLM

项目通过 OpenAI-compatible API 调用大语言模型。

LLM 主要负责：

1. 理解客户上下文
2. 根据客户信息生成自然语言回复
3. 根据销售 Prompt 控制回复风格
4. 根据产品和 CRM 信息生成个性化销售话术

整体调用链：

```text
Python
   ↓
LLMClient
   ↓
OpenAI-compatible API
   ↓
LLM
   ↓
返回销售回复
```

核心封装位于：

```text
llm/client.py
```

---

# 7. Prompt Engineering

项目没有直接将客户消息发送给 LLM，而是构建完整的销售上下文。

Prompt 中包含：

```text
客户信息
+
CRM信息
+
产品信息
+
客户意图
+
历史对话
+
客户最新消息
```

例如：

```text
当前客户信息：

张先生，28岁，上海，互联网从业者……

当前CRM信息：

意向等级：高
跟进状态：重点跟进

当前产品信息：

青春信用卡……
尊享信用卡……

系统识别出的客户意图：

高意向

历史对话：

……

客户最新消息：

那就现在帮我办理吧。
```

然后交给 LLM 生成最终销售回复。

---

# 8. 多轮对话

项目支持多轮销售对话。

系统通过：

```text
ConversationState
```

保存当前对话状态。

主要保存：

```text
customer_id
customer_info
crm_info
current_intent
product_info
history
last_user_message
last_assistant_message
```

因此，客户可以连续进行多轮咨询。

例如：

```text
客户：你们有哪些信用卡？

AI：目前有青春信用卡和尊享信用卡。

客户：青春信用卡年费多少？

AI：青春信用卡年费为0元。

客户：额度大概多少？

AI：青春信用卡预计额度为10000-50000元。

客户：那就现在帮我办理吧。

AI：好的，我可以进一步为您介绍申请流程。
```

系统会将历史对话保存在当前 ConversationState 中。

---

# 9. CRM 自动更新

Agent 会根据客户意图更新 CRM。

例如：

```text
客户：
那就现在帮我办理吧。
```

识别为：

```text
高意向
```

然后更新：

```text
intent_level
    ↓
高

follow_up_status
    ↓
重点跟进

next_action
    ↓
跟进申请流程
```

最终形成：

```text
客户沟通
   ↓
意图识别
   ↓
销售回复
   ↓
CRM更新
   ↓
后续跟进
```

这使项目不只是一个简单的聊天机器人，而是加入了基本的业务闭环。

---

# 10. 项目结构

```text
ai_sales_demo/
│
├── app.py
├── train.py
├── test_api.py
├── test_intent.py
├── test_service.py
├── test_customer_tool.py
├── test_product_tool.py
├── test_crm_tool.py
├── test_agent.py
│
├── config.py
│
├── data/
│   ├── customers.json
│   ├── crm.json
│   └── intent_dataset.csv
│
├── models/
│   └── intent_model.pkl
│
├── llm/
│   └── client.py
│
├── services/
│   └── intent.py
│
├── tools/
│   ├── customer_tool.py
│   ├── product_tool.py
│   └── crm_tool.py
│
└── agent/
    ├── sales_agent.py
    ├── prompt.py
    └── state.py
```

---

# 11. 文件说明

| 文件                        | 作用            |
| ------------------------- | ------------- |
| `app.py`                  | 项目 CLI 启动入口   |
| `train.py`                | 训练客户意图分类模型    |
| `config.py`               | API 和模型配置     |
| `llm/client.py`           | LLM API 封装    |
| `services/intent.py`      | 加载意图分类模型并进行预测 |
| `tools/customer_tool.py`  | 客户信息查询        |
| `tools/product_tool.py`   | 产品信息查询        |
| `tools/crm_tool.py`       | CRM 查询与更新     |
| `agent/sales_agent.py`    | Agent 核心逻辑    |
| `agent/prompt.py`         | Prompt 构建     |
| `agent/state.py`          | 多轮对话状态管理      |
| `data/customers.json`     | 模拟客户数据        |
| `data/crm.json`           | 模拟 CRM 数据     |
| `data/intent_dataset.csv` | 意图分类训练数据      |
| `models/intent_model.pkl` | 训练后的意图分类模型    |

---

# 12. 环境配置

推荐使用 Conda 创建独立环境：

```bash
conda create -n shixi python=3.11
conda activate shixi
```

安装依赖：

```bash
pip install openai python-dotenv joblib scikit-learn
```

---

# 13. API 配置

在项目根目录创建：

```text
.env
```

配置：

```env
OPENAI_API_KEY=your_api_key
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL=gpt-4o-mini
```

项目使用 OpenAI-compatible API，因此也可以根据实际情况替换为其他兼容接口。

**请不要将 `.env` 或 API Key 提交到 GitHub。**

建议 `.gitignore`：

```gitignore
.env
__pycache__/
*.pyc
.vscode/
.idea/
```

---

# 14. 训练意图识别模型

如果需要重新训练模型：

```bash
python train.py
```

训练完成后会生成：

```text
models/intent_model.pkl
```

该文件会在运行时被：

```text
services/intent.py
```

加载。

整体关系：

```text
intent_dataset.csv
       ↓
   train.py
       ↓
训练分类模型
       ↓
intent_model.pkl
       ↓
services/intent.py
       ↓
在线预测
```

---

# 15. 运行项目

直接运行：

```bash
python app.py
```

输入客户 ID：

```text
请输入客户ID（例如 C10001）：C10001
```

开始对话：

```text
客户：你们有哪些信用卡？

AI：目前有青春信用卡和尊享信用卡，两款产品在年费、额度和权益方面有所不同。
```

继续进行多轮对话：

```text
客户：青春信用卡年费多少？

AI：青春信用卡年费为0元。

客户：额度大概多少？

AI：青春信用卡预计额度为10000-50000元。

客户：那就现在帮我办理吧。

AI：好的，我可以进一步为您介绍申请流程。
```

输入：

```text
exit
```

结束对话。

---

# 16. Agent 核心流程

整个项目最核心的执行逻辑可以概括为：

```text
用户输入
   ↓
SalesAgent.process()
   ↓
IntentClassifier
   ↓
识别客户意图
   ↓
选择业务 Tool
   ↓
获取业务数据
   ↓
更新 ConversationState
   ↓
构建 Prompt
   ↓
调用 LLM
   ↓
生成销售回复
   ↓
更新 CRM
   ↓
返回客户
```

---

# 17. 为什么使用 Tool？

项目没有把所有业务逻辑全部交给 LLM。

例如：

```text
“青春信用卡年费是多少？”
```

LLM 不应该自己猜测答案。

而应该：

```text
客户问题
   ↓
判断需要产品信息
   ↓
ProductTool
   ↓
查询真实产品数据
   ↓
返回结果
   ↓
LLM组织语言
```

因此项目遵循一个重要原则：

> **LLM 负责理解和生成，Tool 负责确定性的业务操作。**

这种设计可以降低 LLM 编造业务信息的风险，也方便后续将 JSON 数据替换成数据库或企业 API。

---

# 18. AI Engineer 技术栈

本项目涉及的主要技术：

| 技术                  | 作用           |
| ------------------- | ------------ |
| Python              | 项目开发         |
| LLM                 | 自然语言理解与回复生成  |
| Prompt Engineering  | 控制 LLM 行为    |
| Agent               | 协调模型、工具和业务逻辑 |
| Tool                | 封装确定性的业务操作   |
| TF-IDF              | 文本特征提取       |
| Logistic Regression | 意图分类         |
| OpenAI API          | LLM 调用       |
| JSON                | 模拟业务数据       |
| CRM                 | 销售业务状态管理     |

---

# 19. 当前项目与生产系统的区别

本项目主要用于学习和 Demo 展示，因此对真实企业系统进行了简
