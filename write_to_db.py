import sqlite3
import pandas as pd
import sqlalchemy


def main():
    # 1. Подключаемся к SQLite и получаем учетные данные
    sqlite_conn = sqlite3.connect("creds.db")
    credentials = pd.read_sql("SELECT * FROM access LIMIT 1", sqlite_conn)
    sqlite_conn.close()

    # Извлекаем учетные данные
    db_user = credentials.iloc[0]["user"]
    db_password = credentials.iloc[0]["pass"]
    db_host = credentials.iloc[0]["url"]
    db_port = credentials.iloc[0]["port"]
    db_name = "homeworks"

    # 2. Подключаемся к PostgreSQL
    connection_string = (
        f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    )
    engine = sqlalchemy.create_engine(connection_string)

    # 3. Загружаем датасет и записываем 100 строк
    df_genomic = pd.read_parquet("df_genomic.parquet")
    sample_data = df_genomic.head(100)

    # Записываем в таблицу с фамилией
    table_name = "bazhenova"
    sample_data.to_sql(table_name, engine, if_exists="replace", index=False)

    # 4. Проверяем что записалось
    check_query = pd.read_sql("SELECT * FROM bazhenova LIMIT 5", engine)
    print("Первые 5 строк из таблицы:")
    print(check_query)


if __name__ == "__main__":
    main()
