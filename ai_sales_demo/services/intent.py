import joblib


class IntentClassifier:
    """
    客户意图识别器

    负责加载已经训练好的模型，
    并对客户输入进行意图预测。
    """

    def __init__(self, model_path="models/intent_model.pkl"):
        self.model_path = model_path

        # 加载已经训练好的模型
        self.model = joblib.load(model_path)

    def predict(self, text):
        """
        输入：
            text: 客户说的话

        输出：
            客户意图
        """

        prediction = self.model.predict([text])

        return prediction[0]