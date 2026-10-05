from services.intent import IntentClassifier


def main():

    classifier = IntentClassifier()

    test_sentences = [
        "这张卡有什么优惠？",
        "最高可以申请多少额度？",
        "办理需要手续费吗？",
        "我暂时不需要了",
        "我想申请这张卡",
        "那就现在帮我办理吧"
    ]

    print("=" * 60)
    print("Intent Service 测试")
    print("=" * 60)

    for text in test_sentences:

        intent = classifier.predict(text)

        print(f"\n客户：{text}")
        print(f"意图：{intent}")


if __name__ == "__main__":
    main()