from typing import List, Optional
from datetime import datetime
from string import capwords
import csv, re

CSV_FILE_PATH = './task.csv' 

class Employee:
    def __init__(self, last_name: str, first_name: str, position: str,
                 hire_date: datetime, salary: int, middle_name: Optional[str] = None):
        self.__last_name = last_name
        self.__first_name = first_name
        self.__middle_name = middle_name
        self.__position = position
        self.__hire_date = hire_date
        self.__salary = salary

    @staticmethod
    def parse_date(value: str) -> datetime:
        return datetime.strptime(value, '%d.%m.%Y')
    
    @property
    def last_name(self) -> str:
        return self.__last_name
    
    @property
    def first_name(self) -> str:
        return self.__first_name
    
    @property
    def middle_name(self) -> str:
        return self.__middle_name
    
    @property
    def position(self) -> str:
        return self.__position
    
    @property
    def hire_date(self) -> datetime:
        return self.__hire_date
    
    @property
    def salary(self) -> int:
        return self.__salary
    
    @salary.setter
    def salary(self, value: int):
        if value < 0:
            raise ValueError('Зарплата не может быть отрицательной')
        self.__salary = value
    
    @last_name.setter
    def last_name(self, value: str):
        if len(value) < 2:
            raise ValueError('Фамилия не может состоять из такого количества букв')
        if not re.fullmatch(r'^[А-Яа-яЁё]+$', value):
            raise ValueError('Фамилия должна быть написана кириллицей')
        self.__last_name = capwords(value)

    @first_name.setter
    def first_name(self, value: str):
        if len(value) < 2:
            raise ValueError('Имя не может состоять из такого количества букв')
        if not re.fullmatch(r'^[А-Яа-яЁё]+$', value):
            raise ValueError('Имя должно быть написано кириллицей')
        self.__first_name = capwords(value)

    @middle_name.setter
    def middle_name(self, value: str):
        if not value:
            self.__middle_name = None
        else:
            if len(value) < 3:
                raise ValueError('Отчество не может состоять из такого количества букв')
            if not re.fullmatch(r'^[А-Яа-яЁё]+$', value):
                raise ValueError('Отчество должно быть написано кириллицей')
            self.__middle_name = capwords(value)

    @position.setter
    def position(self, value: str):
        if len(value) < 2:
            raise ValueError('Название должности не может состоять из такого количества букв')
        self.__first_name = value

    def full_name(self) -> str:
        return f'{self.__last_name} {self.__first_name} {self.__middle_name}'


def read_employees_from_csv(file_path: str) -> List[Employee]:
    employees = []
    with open(file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        next(reader)
        for row in reader:
            last_name, first_name, middle_name = row[0].split()
            employee = Employee(
                last_name=last_name,
                first_name=first_name,
                middle_name=middle_name,
                position=row[1],
                hire_date=Employee.parse_date(row[2]),
                salary=int(row[3].replace(' ', ''))
            )
            employees.append(employee)
    return employees


employees = read_employees_from_csv(CSV_FILE_PATH)

# Проверка работы
for emp in employees:
    print(emp.full_name(), emp.position, emp.salary)
