import pandas as pd

# Присвоение имени файла (датасет)
file_name = 'Homo_sapiens.GRCh38.92.csv'

# Загрузка данных в датафрэйм
raw_data = pd.read_csv(file_name)

# Вывод первых 10 строк датасета
print(raw_data.head(10))
