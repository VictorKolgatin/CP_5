from src import api_hh_class, DBManager
from config import host, database, user, password

def main():
    # Запрашиваем пароль и название БД
    password = input('Введите пароль от БД: ')
    name_db = input('Введите название БД')

    # Создаем экземпляр класса DBManager
    db_item = DBManager()

    db_item.create_db(name_db)

    # Создаем экземляр api hh
    api_hh = api_hh_class()

    # Получаем список вакансий
    vac_list = api_hh.get_vacancies()
    # Получаем список работодателей
    emp_list = api_hh.get_employers()


