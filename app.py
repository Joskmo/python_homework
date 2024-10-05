from typing import List
from string import capwords
from texts import START_MSG, WRITE_FILE_MSG, MAN_WOMAN_PREM
from Employee import Employee
import csv, os, time

CSV_FILE_PATH = './task.csv' 
RESULT_DIR = 'results/'

def read_employees_from_csv(file_path: str) -> List[Employee]:
    employees = []
    with open(file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        next(reader)
        for row in reader:
            name_parts = row[0].split()
            last_name = name_parts[0]
            first_name = name_parts[1]
            middle_name = name_parts[2] if len(name_parts) > 2 else None
            employee = Employee(
                last_name=last_name,
                first_name=first_name,
                middle_name=middle_name,
                position=row[1],
                hire_date=Employee.parse_date(row[2]),
                salary=int(row[3].replace(' ', '')),
                sex=capwords(row[4])
            )
            employees.append(employee)
    return employees


def clear():
    if os.system == 'nt':
        os.system('cls')
    else:
        os.system('clear')
    

employees = read_employees_from_csv(CSV_FILE_PATH)
exit_flag = False

while(not exit_flag):
    try:
        print(START_MSG)
        choose = input("Ваш выбор: ")
        if choose == '0':
            flag = False
            while(not flag):
                clear()
                print(WRITE_FILE_MSG)
                choose_write = input("Ваш выбор: ")
                if choose_write == '0': # назад
                    clear()
                    flag = True
                elif choose_write == '1': # json
                    filename_flag = False
                    while(not filename_flag):
                        clear()
                        print("Выбрана запись в .json файл")
                        user_file_name = input("Введите имя файла без расширения (к примеру, employees): ")
                        if user_file_name:
                            filename_flag = True
                            file_name = RESULT_DIR + user_file_name + ".json"
                            Employee.write_to_json(employees, file_name)
                            clear()
                            print(f'Файл записан в: {file_name}')
                        else:
                            print("Проверьте ввод")
                            time.sleep(0.7)
                    flag = True
                elif choose_write == '2': # csv
                    filename_flag = False
                    while(not filename_flag):
                        clear()
                        print("Выбрана запись в .csv файл")
                        user_file_name = input("Введите имя файла без расширения (к примеру, employees): ")
                        if user_file_name:
                            filename_flag = True
                            file_name = RESULT_DIR + user_file_name + ".csv"
                            Employee.write_to_csv(employees, file_name)
                            clear()
                            print(f'Файл записан в: {file_name}')
                        else:
                            print("Проверьте ввод")
                            time.sleep(0.7)
                    flag = True
                else:
                    print('Проверьте ввод')
                    time.sleep(0.7)
                    
        elif choose == '1': # Вывод текущих данных
            clear()
            for emp in employees:
                print(emp.print_everything, '\n')
        elif choose == '2': # Расчёт премии ко дню программиста
            for emp in employees:
                emp.prem_prog()
            clear()
            print('Программистам начислена премия')
        elif choose == '3': # Расчёт премии к 8 марта и 23 февраля
            clear()
            flag = False
            while(not flag):
                clear()
                print(MAN_WOMAN_PREM)
                choose_man_wom = input("Ваш выбор: ")
                if choose_man_wom == '0': # назад
                    clear()
                    flag = True
                elif choose_man_wom == '1': # 23.02
                    flag = True
                    for emp in employees:
                        emp.prem_man()
                    clear()
                    print('Начислены премии мужчинам')
                elif choose_man_wom == '2': # 8.03
                    flag = True
                    for emp in employees:
                        emp.prem_wom()
                    clear()
                    print('Начислены премии женщинам')
                else:
                    print('Проверьте ввод')
                    time.sleep(0.7)
        elif choose == '4': # Расчёт индексации зарплат
            for emp in employees:
                emp.index()
            clear()
            print("Зарплаты проиндексированы")
        elif choose == '5': # Получить список сотрудников, которым положен отпуск
            clear()
            print("Отпуск положен следующим сотрудникам:")
            for emp in employees:
                if emp.rest():
                    print("  ", emp.full_name)
            print()
        elif choose == '9': # Выход из программы
            exit_flag = True
        else:
            clear()
            print("Проверьте введённые данные")

    except ValueError: 
        clear()
        print('Проверьте ввод')

    except KeyboardInterrupt:
        exit_flag = True
        print()

    if exit_flag: 
        print('Выход из программы...')
        time.sleep(0.5)
        clear()
