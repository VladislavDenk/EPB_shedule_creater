import os
import datetime
import sqlite3 as sql
import pandas as pd
from pathlib import Path
from handlers import get_value, write_value

from config import TEAMS

from models import adding_data, create_table_for_team, drop_tables
# from sender_report import send_message, TEAMS, PATH_TO_FILE
from sender_report import send_message


if __name__ == "__main__":
    
    user_year = int(input("Введите год за который необходимо сформировать отчет: "))
    last_day_year = datetime.date(user_year, 12, 31)
    
    print("🧹 Очистка старых таблиц в БД...")
    
    # Формирование списка наименований книг в таблице Excel
    BOOK_TITLES = [f"Оборудование_{team}" for team in TEAMS]
    
    # Удаление таблиц в БД
    drop_tables(BOOK_TITLES)
    
    for i, team in enumerate(TEAMS):
        print(f"Обработка данных компании {team}")
        # Получаем данные о СИ компании
        get_value(name_base=BOOK_TITLES[i], user_date=last_day_year)
        # Создаем файл отчета о состоянии СИ компании
        file_name: str = write_value(book_title=BOOK_TITLES[i], year=user_year)
        # Отправляем письмо с отчетом сотрудникам компании
        # send_message(file_name=file_name, team_name=team)
    
    print("🏁 Все команды обработаны.")