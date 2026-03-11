import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.tree import DecisionTreeClassifier

df = pd.read_csv("data.csv")
# Определение целевой переменной и признаков
X = df.drop('rating', axis=1)  # Все столбцы, кроме 'rating', используются как признаки
y = df['rating']  # 'rating' - целевая переменная (рейтинг)

# Разделение данных на тренировочную и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Дерево решений
model = DecisionTreeClassifier(random_state=42)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

test_df = pd.read_csv("test_df.csv")
test_df = test_df.drop('rating', axis=1)
test_df = test_df[test_df.columns]

predicted_rating = model.predict(test_df)
priv_df = pd.read_csv("priv.csv")

for index in priv_df.index:
    print(f"{priv_df['review'][index]}: {predicted_rating[index]}\n")



