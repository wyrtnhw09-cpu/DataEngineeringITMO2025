import pandas as pd
from pathlib import Path


def download_and_validate_source(data_url: str, raw_data_path: str) -> pd.DataFrame:
    Path(raw_data_path).parent.mkdir(parents=True, exist_ok=True)

    print(f"Загружаем данные из: {data_url}")
    df = pd.read_csv(data_url)

    df.to_csv(raw_data_path, index=False)
    print(f"Сырые данные сохранены в: {raw_data_path}")
    print(f"Размер данных: {df.shape[0]} строк, {df.shape[1]} колонок")

    return df


def validate_raw_data(df: pd.DataFrame) -> bool:
    required_columns = ["gene_id", "seqname", "start", "end"]
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Отсутствует колонка: {col}")
    print("Валидация сырых данных пройдена")
    return True
