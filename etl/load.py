import pandas as pd
import sqlite3
from pathlib import Path
import warnings

# Игнорируем все предупреждения
warnings.filterwarnings("ignore")


def load_to_database(
    df: pd.DataFrame, db_path: str, table_name: str = "genes", sample_size: int = 100
):
    print(f"Загружаем {sample_size} строк в базу данных...")

    # Создаем датафрейм только с 2 колонками
    simple_df = pd.DataFrame(
        {
            "gene_id": df["gene_id"].head(sample_size).astype(str),
            "seqname": df["seqname"].head(sample_size).astype(str),
        }
    )

    print(f"Загружаем только 2 колонки: gene_id, seqname")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # Создаем таблицу вручную
        cursor.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                gene_id TEXT,
                seqname TEXT
            )
        """
        )

        # Очищаем таблицу
        cursor.execute(f"DELETE FROM {table_name}")

        # Вставляем данные построчно
        for index, row in simple_df.iterrows():
            cursor.execute(
                f"""
                INSERT INTO {table_name} (gene_id, seqname)
                VALUES (?, ?)
            """,
                (str(row["gene_id"]), str(row["seqname"])),
            )

        conn.commit()
        print(f"Данные загружены в базу {db_path}")
        print(f"Таблица '{table_name}' создана с {sample_size} строками")

    except Exception as e:
        print(f"Ошибка при загрузке в БД: {e}")
        raise
    finally:
        conn.close()


def save_to_parquet(df: pd.DataFrame, output_path: str):
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    # Игнорируем ошибки при сохранении в parquet
    try:
        df.to_parquet(output_path, index=False)
        print(f"Данные сохранены в Parquet: {output_path}")
    except Exception as e:
        print(f"Предупреждение при сохранении Parquet: {e}")
        # Пробуем сохранить только часть данных
        safe_columns = ["gene_id", "seqname", "start", "end", "gene_name"]
        available_columns = [col for col in safe_columns if col in df.columns]
        df_safe = df[available_columns].copy()
        df_safe.to_parquet(output_path, index=False)
        print(f"Данные сохранены в Parquet (только безопасные колонки): {output_path}")
