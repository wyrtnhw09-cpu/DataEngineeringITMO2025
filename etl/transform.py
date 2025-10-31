import pandas as pd


def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    print("Начинаем трансформацию данных...")
    df_transformed = df.copy()

    string_columns = ["gene_id", "transcript_id", "seqname", "gene_biotype"]
    for col in string_columns:
        if col in df_transformed.columns:
            df_transformed[col] = df_transformed[col].astype("string")

    numeric_columns = ["start", "end"]
    for col in numeric_columns:
        if col in df_transformed.columns:
            df_transformed[col] = pd.to_numeric(df_transformed[col], errors="coerce")

    if all(col in df_transformed.columns for col in ["start", "end"]):
        df_transformed["gene_length"] = df_transformed["end"] - df_transformed["start"]

    print("Трансформация данных завершена")
    return df_transformed
