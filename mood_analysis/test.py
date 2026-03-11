import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

df = pd.read_csv("sber_app.csv")
df = df.dropna(axis=0, how='any')
df = df.drop(['Unnamed: 0', 'userName', 'developerResponse'], axis=1)

priv_df = df.iloc[5000:5862]
priv_df.to_csv('priv.csv')
# Создание объекта TfidfVectorizer
vectorizer = TfidfVectorizer()

# Преобразование текстов в векторы TF-IDF
X_title = vectorizer.fit_transform(df['title'])
df_title = pd.DataFrame(X_title.toarray(), columns=vectorizer.get_feature_names_out())

X_review = vectorizer.fit_transform(df['review'])
df_review = pd.DataFrame(X_review.toarray(), columns=vectorizer.get_feature_names_out())

df = pd.concat([df.reset_index(drop=True), df_title, df_review], axis=1).drop(columns=['title', 'review'])
df['isEdited'] = np.where(df['isEdited'] == True, 1, 0)
df['date'] = pd.to_datetime(df['date'])

# Извлечение числовых признаков из даты (например, день, месяц, год)
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month
df['day'] = df['date'].dt.day
df['hour'] = df['date'].dt.hour
df['minute'] = df['date'].dt.minute

# Удаление исходного столбца 'date'
df = df.drop('date', axis=1)

new_df = df.iloc[5000:5862]
df = df.iloc[0:5000]

rating_1 = df[df['rating'] == 1]
rating_2 = df[df['rating'] == 2]
rating_3 = df[df['rating'] == 3]
rating_4 = df[df['rating'] == 4]
rating_5 = df[df['rating'] == 5]

rat_1 = rating_1.sample(len(rating_5))
rat_2 = rating_2.sample(len(rating_5), replace=True)
rat_3 = rating_3.sample(len(rating_5), replace=True)
rat_4 = rating_4.sample(len(rating_5), replace=True)
df = pd.concat([rat_1, rat_2, rat_3, rat_4, rating_5])

df.to_csv('data.csv')
new_df.to_csv('test_df.csv')
