import pandas as pd

import numpy as np

# Загрузка данных в датафрэйм
data = pd.read_csv(
    "/Users/wyrtnh.w/DataEngineeringITMO2025/data/Homo_sapiens.GRCh38.92.csv"
)

# Вывод первых 10 строк датасета
data.head(10)

data.isnull().sum()

missing_data = (data.isnull().sum() / len(data)) * 100
missing_data

# Удаляем столбцы, где пропусков больше 50%
data = data.loc[:, data.isnull().mean() <= 0.5]

missing_data = (data.isnull().sum() / len(data)) * 100
missing_data

data

df = data.copy()

# Проверяем типы
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

pip install fastparquet

# Сохраняем в Parquet
df.to_parquet('genome_data.parquet', index=False, engine='fastparquet')