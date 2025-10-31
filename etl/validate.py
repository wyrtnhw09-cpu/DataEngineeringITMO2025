import pandas as pd


def validate_dataframe_structure(df: pd.DataFrame) -> bool:
    required_columns = ["gene_id", "seqname", "start", "end"]
    missing_columns = [col for col in required_columns if col not in df.columns]

    if missing_columns:
        raise ValueError(f"Отсутствуют колонки: {missing_columns}")

    print("Структура данных корректна")
    return True
