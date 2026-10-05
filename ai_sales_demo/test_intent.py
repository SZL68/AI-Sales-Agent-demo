import joblib


MODEL_PATH = "models/intent_model.pkl"


def main():
    print("=" * 60)
    print("客户意图识别测试")
    print("=" * 60)

    # 加载训练好的模型
    model = joblib.load(MODEL_PATH)

    test_sentences = [
        "这张信用卡有什么优惠？",
        "我想知道最高额度是多少",
        "办理这张卡需要收费吗",
        "我现在不想申请了",
        "我想申请这张信用卡",
        "那就现在帮我办理吧",
        "这个产品适合什么人？",
        "我暂时没有需求"
    ]

    predictions = model.predict(test_sentences)

    for text, prediction in zip(test_sentences, predictions):
        print(f"\n客户话术：{text}")
        print(f"预测意图：{prediction}")


if __name__ == "__main__":
    main()