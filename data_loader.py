# скрипт выгрузки файла из Google Drive:
import pandas as pd
FILE_ID = "1eUWO6tAac-u-a1IrIqXJWgKE_4JJyjWt"
file_url = f"https://drive.google.com/uc?id={FILE_ID}"
raw_data = pd.read_csv(file_url)
print(raw_data.head(10)) # выводим первые 10 строк датасета
