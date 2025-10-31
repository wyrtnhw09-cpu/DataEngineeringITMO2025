import pandas as pd
import numpy as np
pip install gdown
import gdown

# Загрузка данных в датафрэйм
gdown.download('https://drive.google.com/uc?id=1eUWO6tAac-u-a1IrIqXJWgKE_4JJyjWt', 'data.csv', quiet=False)
data = pd.read_csv('data.csv')

data.head(10)

# Выводим количество пропущенных значений в датасете
data.isnull().sum()

# Выводим количество пропущенных значений в процентах
missing_data = (data.isnull().sum() / len(data)) * 100
missing_data

# Удаляем столбцы, где пропусков больше 50%
data = data.loc[:, data.isnull().mean() <= 0.5]

missing_data = (data.isnull().sum() / len(data)) * 100
missing_data

data

# Копируем датасет для проведения манипуляций над данными в нем
df = data.copy()

# Выводим типы данных
df.dtypes

# Числовые колонки
df['basic'] = df['basic'].fillna(-1).astype(int)
df['exon_number'] = df['exon_number'].fillna(-1).astype(int)
df['transcript_version'] = df['transcript_version'].fillna(-1).astype(int)

# Все текстовые колонки делаем строками
text_cols = ['seqname', 'source', 'feature', 'score', 'strand', 'frame', 
             'gene_biotype', 'transcript_biotype', 'transcript_support_level',
             'gene_id', 'gene_name', 'gene_source', 'transcript_id', 
             'transcript_name', 'transcript_source']

for col in text_cols:
    df[col] = df[col].fillna('unknown').astype(str)

# Проверяем типы
df.dtypes

pip install parquet

df.to_parquet('df_genomic.parquet', index=False)

completeness = (1 - df.isnull().mean()).round(4)
print("Completeness (полнота данных):")
print(completeness)

# Проверяем ключевые идентификаторы
key_columns = ['gene_id', 'transcript_id', 'gene_name']
uniqueness = {}

for col in key_columns:
    if col in df.columns:
        total = len(df[col])
        unique = df[col].nunique()
        uniqueness[col] = round(unique / total, 4)

print("Uniqueness (уникальность):")
for col, score in uniqueness.items():
    print(f"{col}: {score}")

    # Дубликаты по всем колонкам
total_rows = len(df)
duplicate_rows = df.duplicated().sum()
duplication_rate = round(duplicate_rows / total_rows, 4)

print(f"Duplication Rate (уровень дубликатов): {duplication_rate}")
print(f"Дубликатов: {duplicate_rows} из {total_rows} строк")

# Дубликаты по ключевым колонкам
if 'gene_id' in df.columns:
    gene_duplicates = df['gene_id'].duplicated().sum()
    gene_duplication_rate = round(gene_duplicates / total_rows, 4)
    print(f"Duplication Rate по gene_id: {gene_duplication_rate}")

    # Для числовых колонок
numeric_cols = ['start', 'end', 'basic', 'exon_number', 'transcript_version']
outlier_ratio = {}

for col in numeric_cols:
    if col in df.columns:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        outliers = ((df[col] < lower_bound) | (df[col] > upper_bound)).sum()
        outlier_ratio[col] = round(outliers / len(df), 4)

print("Outlier Ratio (доля выбросов):")
for col, ratio in outlier_ratio.items():
    print(f"{col}: {ratio}")

import matplotlib.pyplot as plt

# Прроверка выбросов
for col in ['start', 'end', 'exon_number']:
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    outliers = ((df[col] < Q1 - 1.5*(Q3-Q1)) | (df[col] > Q3 + 1.5*(Q3-Q1))).sum()
    print(f"{col}: {outliers} выбросов")

# Простой boxplot
plt.figure(figsize=(8, 4))
df[['start', 'end']].boxplot()
plt.title("Выбросы в координатах генов")
plt.show()

# Гистограмма количества экзонов
plt.figure(figsize=(8, 4))
plt.hist(df['exon_number'], bins=20, color='lightblue', edgecolor='black')
plt.title("Распределение экзонов")
plt.xlabel("Количество экзонов")
plt.ylabel("Частота")
plt.show()

# Типы генов
print("Топ 10 типов генов:")
print(df['gene_biotype'].value_counts().head(10))

# Типы транскриптов
print("\nТоп 10 типов транскриптов:")
print(df['transcript_biotype'].value_counts().head(10))

# Особенности генов
print(f"\nОбзор генов:")
print(f"Всего уникальных генов: {df['gene_id'].nunique()}")
print(f"Всего уникальных имен генов: {df['gene_name'].nunique()}")

# Простые корреляции между числовыми признаками
numeric_cols = ['start', 'end', 'basic', 'exon_number', 'transcript_version']
numeric_df = df[numeric_cols]

print("Корреляции:")
print(numeric_df.corr().round(3))

# Самая сильная корреляция
corr_matrix = numeric_df.corr()
strong_corr = corr_matrix.unstack().sort_values(ascending=False)
strong_corr = strong_corr[strong_corr < 0.99]  # убираем корреляцию с собой
print(f"\nСамая сильная корреляция: {strong_corr.index[0]} = {strong_corr.iloc[0]:.3f}")

# Длина гена/транскрипта
df['gene_length'] = df['end'] - df['start']
print(f"Средняя длина гена: {df['gene_length'].mean():.0f} пар оснований")

# Количество экзонов на транскрипт
if 'exon_number' in df.columns:
    exon_stats = df.groupby('transcript_id')['exon_number'].max().describe()
    print(f"\nСтатистика экзонов на транскрипт:")
    print(f"Мин: {exon_stats['min']}, Макс: {exon_stats['max']}, Среднее: {exon_stats['mean']:.1f}")

# Признак "длинный ген"
df['is_long_gene'] = (df['gene_length'] > df['gene_length'].median()).astype(int)
print(f"\nДлинные гены (> медианы): {df['is_long_gene'].mean():.1%}")

# Источники генов
print("Источники аннотаций генов:")
print(df['source'].value_counts())

# Уровень поддержки транскриптов
print("\nУровень поддержки транскриптов:")
print(df['transcript_support_level'].value_counts())