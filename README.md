# Data Engineering_ITMO 2025

Ссылка на датасет: https://drive.google.com/drive/folders/128p_E86Ceer08JPGr8vKWPMkmyKI3pSv?usp=share_link

## Описание

Этот проект предназначен для работы с датасетом Homo sapiens. Скрипт `data_loader.py` загружает данные из CSV-файла и выводит первые 10 строк.

## Установка

Для установки зависимостей используйте [Poetry](https://python-poetry.org/):
   bash
   poetry run python dataloader.py

### Ожидаемый результат

Скрипт загрузит данные из файла `Homosapiens.GRCh38.92.csv` и выведет первые 10 строк датасета в консоль.
<img width="1468" height="699" alt="Снимок экрана 2025-10-28 в 1 47 01 AM" src="https://github.com/user-attachments/assets/02101a84-8b8e-4cc6-8195-d71a3e68ec58" />






## Установка зависимостей

Этот проект использует `Poetry` для управления зависимостями. Для установки необходимых зависимостей выполните следующие шаги:
1. Требования: python версии 3.13 или выше
2. Убедитесь, что у вас установлен `Poetry`. Если он не установлен, вы можете установить его, следуя [официальной документации Poetry](https://python-poetry.org/docs/#installation)
3. Клонируйте репозиторий:
   bash
   git clone https://github.com/<ваш-логин>/<ваш-репозиторий>.git
   cd <ваш-репозиторий>
4. Установите зависимости:
   bash
   poetry install
   5. Для проверки установленных зависимостей вы можете использовать:
   bash
   poetry show
