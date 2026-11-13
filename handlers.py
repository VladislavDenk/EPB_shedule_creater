import os
import datetime
import json
import sqlite3 as sql
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Side
from openpyxl.worksheet.dimensions import ColumnDimension

from pathlib import Path

from config import (
    TEAMS, 
    PATH_TO_FILE,  
    TITLE_COLUMN_WITH_ADDRESSES, 
    DB_NAME
)

from models import adding_data, create_table_for_team, drop_tables
# from sender_report import send_message, TEAMS, PATH_TO_FILE
from sender_report import send_message

today: datetime = datetime.datetime.now()

# Получение адресов объектов
addresses = pd.read_excel(
    PATH_TO_FILE, 
    sheet_name=0, 
    header=1, 
    usecols=[10, ]
)
# Формирование списка адресов существующих объектов
index_last_rows = addresses.tail(1).index[0]
addresses_list = [addresses.iloc[df][TITLE_COLUMN_WITH_ADDRESSES] for df in range(index_last_rows)]


# def create_addresses_dict(addresses_list: list):
#     addresses_dict = {}
#     for i, addresses in enumerate(addresses_list):
#         addresses_dict.setdefault(i, addresses)
        
#     # print(json.dumps(addresses_dict, indent=4, ensure_ascii=False))
#     need_azs = json.dumps(addresses_dict, indent=4, ensure_ascii=False)
#     prefix = "АГЗС № 54061"
#     if prefix in need_azs:
#         print(True)

#     return json.dumps(addresses_dict, indent=4, ensure_ascii=False)


# def print_addreses(prefix: str, address: str):
#     print(f"{prefix} - {address}")
    

def get_value(name_base: str, user_date: datetime.date):
    "Получение значений из файла и запись их в БД"
    books = pd.read_excel(PATH_TO_FILE, sheet_name=name_base)
    
    # Формирование списка объектов под ЭПБ
    for i, date in enumerate(books[25]):
        # if isinstance(date, datetime) and date.date() <= user_date:
        if isinstance(date, datetime.datetime) and date.date() <= user_date:
            # print(date.date())
            prefix = books[1][i].strip()
            # address = next((item for item in addresses_list if item.startswith(prefix)), None)
            address = next((item for item in addresses_list if prefix in item), None)
            name_equipment = books[3][i]
            factory_number = books[4][i]
            if isinstance(books[8][i], datetime.datetime):
                manufacture_date = books[8][i].strftime("%d.%m.%Y")
            else:
                manufacture_date = books[8][i]
            # work_type = books[3][i]
            location = address
            epb_date = books[25][i].strftime("%d.%m.%Y")
            note = None
            adding_data(
                name=name_equipment,
                number=factory_number,
                manufacture_date=manufacture_date,
                work_type="ЭПБ",
                location=location,
                epb_date=epb_date,
                note=note,
                team_name=name_base
            )
            
    # Формирование списка объектов под тех. освидетельствование
    for i, date in enumerate(books[17]):
            if isinstance(date, datetime.datetime) and date.date() <= user_date:
            
                # Проверка на наличие записи "Эксперты" в колонке
                executor = books[18][i]
                if not (isinstance(executor, str) and executor.strip().lower() == "эксперты"):
                        continue
                
                prefix = books[1][i].strip()
                # address = next((item for item in addresses_list if item.startswith(prefix)), None)
                address = next((item for item in addresses_list if prefix in item), None)
                name_equipment = books[3][i]
                factory_number = books[4][i]
                if isinstance(books[8][i], datetime.datetime):
                    manufacture_date = books[8][i].strftime("%d.%m.%Y")
                else:
                    manufacture_date = books[8][i]
                work_type = "Тех. освидетельствование"
                location = address
                epb_date = books[17][i].strftime("%d.%m.%Y")
                note = None
                adding_data(
                    name=name_equipment,
                    number=factory_number,
                    manufacture_date=manufacture_date,
                    work_type=work_type,
                    location=location,
                    epb_date=epb_date,
                    note=note,
                    team_name=name_base
                )
        

def write_value(book_title: str, year: str) -> str:
    "Запись данных в файл формата .xlsx с заданной шириной столбцов"
    conn = sql.connect(DB_NAME)
    query = "SELECT * FROM {}".format(book_title)
    data = pd.read_sql_query(query, conn)
    
    file_name = f"График ЭПБ на {year}г. -  {book_title.split("_")[1]}.xlsx"
    with pd.ExcelWriter(file_name, engine='openpyxl') as writer:
        # Экспортируем данные
        data.to_excel(writer, index=False, sheet_name=book_title)
        
        # Получаем доступ к рабочей книге и листу
        wb = writer.book
        ws = writer.sheets[book_title]
        
        # Задаем ширину столбцов
        column_widths = {
            "A": 5, # № п/п
            "B": 30, # Наименование ТУ (марка, тип)
            "C": 15, # Заводской номер
            "D": 14, # Год изготовления
            "E": 12, # Вид работ
            "F": 35, # Местонахождения
            "G": 14, # Дата ЭПБ
            "H": 24, # Примечание
        }    
        
        # Создаем стиль границ
        thin_border = Border(
            left=Side(border_style='thin', color='00000000'),
            right=Side(border_style='thin', color='00000000'),
            top=Side(border_style='thin', color='00000000'),
            bottom=Side(border_style='thin', color='00000000'),
        ) 
        
        # Применяем заданную щирину
        for column, width in column_widths.items():
            ws.column_dimensions[column].width =  width
            
            # Применяем выравнивание и перенос текста для всего столбца
            for row in range(1, ws.max_row + 1):
                cell = ws[f'{column}{row}']
                cell.alignment = Alignment(
                    horizontal='center',
                    vertical='center',
                    wrap_text=True,
                )
                # Добавлем границы ячейкам
                cell.border = thin_border
    
    print(f"✅ Экспорт данных компании {book_title.split("_")[1]} прошел успешно!")
    conn.close()
    return file_name
