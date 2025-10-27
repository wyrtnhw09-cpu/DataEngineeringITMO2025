import pandas as pd

import numpy as np

# Загрузка данных в датафрэйм
df = pd.read_csv(
    "/Users/wyrtnh.w/DataEngineeringITMO2025/data/Homo_sapiens.GRCh38.92.csv"
)

# Вывод первых 10 строк датасета
df.head(10)

df.isnull().sum()

missing_data = (df.isnull().sum() / len(df)) * 100
missing_data

# Удаляем столбцы, где пропусков больше 50%
df = df.loc[:, df.isnull().mean() <= 0.5]

missing_data_2 = (df.isnull().sum() / len(df)) * 100
missing_data_2

df.dtypes

# Столбцы с float, которые должны быть int
df["basic"] = df["basic"].fillna(-1).astype(int)
df["exon_number"] = df["exon_number"].fillna(-1).astype(int)
df["transcript_version"] = df["transcript_version"].fillna(-1).astype(int)

# Столбцы с повторяющимися текстовыми значениями
categorical_cols = [
    "seqname",
    "source",
    "feature",
    "strand",
    "frame",
    "gene_biotype",
    "transcript_biotype",
    "transcript_support_level",
]

for col in categorical_cols:
    df[col] = df[col].astype("category")

    # Обычные текстовые столбцы
text_cols = [
    "gene_id",
    "gene_name",
    "gene_source",
    "transcript_id",
    "transcript_name",
    "transcript_source",
]

for col in text_cols:
    df[col] = df[col].astype(str)

    df.dtypes
