import pandas as pd
import numpy as np

# Присвоение имени файла (датасет)
dataset = "/Users/wyrtnh.w/DataEngineeringITMO2025/data/Homo_sapiens.GRCh38.92.csv"

# Загрузка данных в датафрэйм
df = pd.read_csv(dataset)

# Вывод первых 10 строк датасета
print(df.head(10))

# Копируем датасет, чтобы не вносить изменения непосредственно в него
df_copy = df.copy()

# Вычисляем общее количество строк
total = len(df_copy)

# Вычисляем долю пропусков в каждом столбце
missing_percent_df_copy = (df_copy.isnull().sum() / len(df_copy)) * 100

# Удаляем столбцы с высоким процентом пропусков из df
threshold = 50
columns_to_drop = missing_percent_df_copy[
    missing_percent_df_copy > threshold
].index.tolist()

# Добавляем дополнительные столбцы для удаления, а именно source, gene_source, transcript_source, score, frame, т. к. они не несут важной информации
additional_columns_to_drop = [
    "source",
    "gene_source",
    "transcript_source",
    "score",
    "frame",
]
columns_to_drop.extend(additional_columns_to_drop)

# Удаляем все указанные столбцы
df_copy_cleaned = df_copy.drop(columns=columns_to_drop)

# Приведение типов для числовых столбцов
df_copy_cleaned["start"] = df_copy_cleaned["start"].astype("int32")
df_copy_cleaned["end"] = df_copy_cleaned["end"].astype("int32")

# Для столбцов с пропусками используем pandas nullable types
df_copy_cleaned["basic"] = df_copy_cleaned["basic"].astype(
    "Int8"
)  # бинарный признак (1/NaN)
df_copy_cleaned["exon_number"] = df_copy_cleaned["exon_number"].astype("Int16")
df_copy_cleaned["gene_version"] = df_copy_cleaned["gene_version"].astype("Int8")
df_copy_cleaned["transcript_version"] = df_copy_cleaned["transcript_version"].astype(
    "Int8"
)

# Обработка transcript_support_level (может содержать смешанные типы)
df_copy_cleaned["transcript_support_level"] = pd.to_numeric(
    df_copy_cleaned["transcript_support_level"], errors="coerce"
).astype("Int8")

# Категориальные столбцы
categorical_columns = [
    "seqname",
    "feature",
    "strand",
    "gene_biotype",
    "transcript_biotype",
]
for col in categorical_columns:
    df_copy_cleaned[col] = df_copy_cleaned[col].astype("category")

    # Строковые столбцы
string_columns = ["gene_id", "gene_name", "transcript_id", "transcript_name"]
for col in string_columns:
    df_copy_cleaned[col] = df_copy_cleaned[col].astype("string")

    df_copy_cleaned.to_parquet
