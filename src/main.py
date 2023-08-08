from src import api_hh_class, DBManager
from config import HOST, DBNAME, user, password, dbname  # получать констаны из конфига


def main():
    # Запрашиваем пароль и название БД
    # password = input('Введите пароль от БД: ') # не нужно, берется из конфига
    # name_db = input('Введите название БД') # не нужно, берется из конфига

    # Создаем экземпляр класса DBManager
    db_item = DBManager()
    db_item.create_db(name_db)

    # Создаем экземляр api hh
    api_hh = api_hh_class()

    # Получаем список вакансий
    vac_list = api_hh.get_vacancies()
    # Получаем список работодателей
    emp_list = api_hh.get_employers()
    keyword = input("введите ключевое слово для поиска: ")
    db_item.get_vacancies_with_keyword(keyword)
