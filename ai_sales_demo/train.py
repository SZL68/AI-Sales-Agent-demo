import os
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report


# ============================================================
# 1. 基本配置
# ============================================================

DATA_PATH = "data/intent_dataset.csv"
MODEL_DIR = "models"
MODEL_PATH = os.path.join(MODEL_DIR, "intent_model.pkl")


# ============================================================
# 2. 读取训练数据
# ============================================================

print("=" * 60)
print("1. 读取数据")
print("=" * 60)

df = pd.read_csv(DATA_PATH)

print(f"数据量：{len(df)}")
print(f"字段：{list(df.columns)}")
print("\n各类别数量：")
print(df["label"].value_counts())


# ============================================================
# 3. 划分训练集和测试集
# ============================================================

X = df["text"]
y = df["label"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print("\n" + "=" * 60)
print("2. 数据集划分")
print("=" * 60)

print(f"训练集：{len(X_train)}")
print(f"测试集：{len(X_test)}")


# ============================================================
# 4. 构建模型
# ============================================================

model = Pipeline([
    (
        "tfidf",
        TfidfVectorizer(
            analyzer="char",
            ngram_range=(1, 3)
        )
    ),
    (
        "classifier",
        LogisticRegression(
            max_iter=1000,
            random_state=42
        )
    )
])


# ============================================================
# 5. 模型训练
# ============================================================

print("\n" + "=" * 60)
print("3. 开始训练模型")
print("=" * 60)

model.fit(X_train, y_train)

print("模型训练完成！")


# ============================================================
# 6. 模型评估
# ============================================================

print("\n" + "=" * 60)
print("4. 模型评估")
print("=" * 60)

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

print(f"\nAccuracy: {accuracy:.4f}")

print("\nClassification Report:")
print(
    classification_report(
        y_test,
        y_pred,
        zero_division=0
    )
)


# ============================================================
# 7. 保存模型
# ============================================================

os.makedirs(MODEL_DIR, exist_ok=True)

joblib.dump(model, MODEL_PATH)

print("\n" + "=" * 60)
print("5. 保存模型")
print("=" * 60)

print(f"模型已经保存到：{MODEL_PATH}")