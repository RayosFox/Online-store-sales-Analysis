# 🛍 Анализ продаж интернет-магазина (SQL + DataLens)

## 📌 О проекте
Анализ 100 000 заказов интернет-магазина с использованием SQL и построение интерактивного дашборда в DataLens.

## 🛠 Технологии
- **Python** (pandas, sqlite3) — загрузка и подготовка данных
- **SQL** (оконные функции, CTE, JOIN) — анализ данных
- **DataLens** — интерактивный дашборд

## 📊 Ключевые выводы
- **Общая выручка:** 13.2 млн руб.
- **Всего заказов:** 97 276
- **Самые продаваемые категории:** beleza_saude, relogios_presentes, informatica_acessorios
- **Пик продаж:** ноябрь 2017

## 🔗 Интерактивный дашборд
[Ссылка на дашборд в DataLens]([твоя_ссылка](https://datalens.yandex/fpzuzba300tiz))

## 📁 Файлы
| Файл | Описание |
|------|----------|
| `load_to_sqlite.py` | Загрузка CSV в SQLite |
| `run_sql_advanced.py` | Сложные SQL-запросы |
| `dashboard_data.csv` | Данные для дашборда |

## 🚀 Запуск проекта
```bash
pip install pandas sqlite3
python load_to_sqlite.py
python run_sql_advanced.py
