import argparse
import sys
import os
import warnings

# Игнорируем предупреждения pandas
warnings.filterwarnings("ignore")

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from etl.extract import download_and_validate_source, validate_raw_data
from etl.transform import transform_data
from etl.load import load_to_database, save_to_parquet
from etl.validate import validate_dataframe_structure


def run_etl_pipeline(
    data_url: str, db_path: str = "data/genes.db", sample_size: int = 100
):
    print("Запуск ETL пайплайна...")

    try:
        # Extract
        print("ЭТАП 1: EXTRACT")
        raw_data_path = "data/raw/genome_data.csv"
        df_raw = download_and_validate_source(data_url, raw_data_path)
        validate_raw_data(df_raw)
        validate_dataframe_structure(df_raw)

        # Transform
        print("ЭТАП 2: TRANSFORM")
        df_transformed = transform_data(df_raw)

        # Load
        print("ЭТАП 3: LOAD")
        load_to_database(df_transformed, db_path, sample_size=sample_size)
        save_to_parquet(df_transformed, "data/processed/genome_data.parquet")

        print("\nETL пайплайн успешно завершен!")
        print("Результаты:")
        print(f"   - Сырые данные: {raw_data_path}")
        print(f"   - База данных: {db_path} (100 строк)")
        print(f"   - Parquet файл: data/processed/genome_data.parquet")

    except Exception as e:
        print(f"Ошибка в ETL пайплайне: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="ETL пайплайн для геномных данных")
    parser.add_argument("data_url", help="Путь к исходным данным")
    parser.add_argument("--db-path", default="data/genes.db", help="Путь к SQLite базе")
    parser.add_argument(
        "--sample-size", type=int, default=100, help="Количество строк для БД"
    )

    args = parser.parse_args()

    run_etl_pipeline(args.data_url, args.db_path, args.sample_size)


if __name__ == "__main__":
    main()
