from datetime import datetime
from typing import Optional
from string import capwords
from dateutil.relativedelta import relativedelta
import csv, json, re

class Employee:
    def __init__(self, last_name: str, first_name: str, position: str, hire_date: datetime,
                 salary: int, sex: str, middle_name: Optional[str] = None):
        self.__last_name = last_name
        self.__first_name = first_name
        self.__middle_name = middle_name
        self.__position = position
        self.__hire_date = hire_date
        self.__salary = salary
        self.__sex = sex
        self.__premium = 0

    @staticmethod
    def write_to_json(employees, filename):
        with open(filename, mode='w', encoding='utf-8') as file:
            json.dump([employee.to_dict() for employee in employees], file, ensure_ascii=False, indent=4)
            
    @staticmethod
    def write_to_csv(employees, filename):
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=employees[0].to_dict().keys(), delimiter=';')
            writer.writeheader()
            for employee in employees:
                writer.writerow(employee.to_dict())

    @staticmethod
    def parse_date(value: str) -> datetime:
        return datetime.strptime(value, '%d.%m.%Y')
    
    @staticmethod
    def wage_fund(employees: list) -> int:
        sum = 0
        for emp in employees:
            sum += emp.salary * 12 + emp.premium
        return sum
    
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
    
    @property
    def sex(self) -> str:
        return self.__sex
    
    @property
    def premium(self) -> int:
        return self.__premium
    
    @property
    def full_name(self) -> str:
        return f'{self.__last_name} {self.__first_name}{(" " + self.__middle_name) if self.__middle_name else ""}'
    
    @property
    def print_everything(self) -> str:
        return f'''Сотрудник {self.full_name}: 
    Должность: {self.__position} 
    Дата найма: {self.__hire_date.strftime('%d.%m.%Y')}
    Оклад: {self.__salary}
    Пол: {self.__sex}
    Размер премии: {self.__premium if self.__premium else 0}'''
    
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

    @hire_date.setter
    def hire_date(self, value: str):
        date = self.parse_date(value)
        low_date = datetime(2000, 1, 1)
        if (date > datetime.now().strftime('%d.%m.%Y') or date < low_date):
            raise ValueError('Введена неверная дата')
        self.__hire_date = date

    @salary.setter
    def salary(self, value: int):
        if value < 0:
            raise ValueError('Зарплата не может быть отрицательной')
        self.__salary = value

    @sex.setter
    def sex(self, value: str):
        if capwords(value) != 'М' or capwords(value) != 'Ж':
            raise ValueError('Пол должен быть указан в формате М/Ж')
        self.__sex = value
    
    def prem_prog(self):
        if 'программист' in self.__position:
            self.__premium += self.__salary * 0.03
        
    def prem_wom(self) -> int:
        if self.__sex == 'Ж':
            self.__premium += 2000

    def prem_man(self) -> int:
        if self.__sex == 'М':
            self.__premium += 2000
    
    def index(self):
        if relativedelta(datetime.now(), self.__hire_date).years >= 10:
            self.__salary = round(self.__salary * 1.07)
        else:
            self.__salary = round(self.__salary * 1.05)
        
    def rest(self) -> bool:
        difference = relativedelta(datetime.now(), self.__hire_date)
        if difference.years > 0 or difference.months > 5:
            return True
        else:
            return False
    
    def to_dict(self) -> dict:
        return {
            "ФИО": self.full_name,
            "Должность": self.__position,
            "Дата найма": datetime.strftime(self.__hire_date, '%d.%m.%Y'),
            "Оклад": self.__salary,
            "Пол": self.__sex,
            "Размер премии": self.__premium
        }
