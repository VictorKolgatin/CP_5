from src.DBManager import DBManager
from src.api_hh_class import HeadHunterAPI
from src.queries import GET_COMPANIES_AND_VACANCIES_COUNT, GET_ALL_VACANCIES, GET_AVG_SALARY, \
    GET_VACANCIES_WITH_HIGHER_SALARY
from src.utils import write_csv


def main():
    # Создаем экземпляр класса DBManager
    db_item = DBManager()

    # Создаем экземляр api hh
    api_hh = HeadHunterAPI()

    # Получаем список вакансий и работодателей
    vac_list = api_hh.get_vacancies_and_format()
    emp_list = api_hh.get_employers()

    # Записываем полученные данные в файл csv

    write_csv('vacancies', vac_list)
    write_csv('employers', emp_list)

    # Выполнение sql запросов.
    # Получает список всех компаний и количество вакансий у каждой компании.
    print(db_item.execute(GET_COMPANIES_AND_VACANCIES_COUNT))

    # Получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.
    print(db_item.execute(GET_ALL_VACANCIES))

    # Получает среднюю зарплату по вакансиям.
    print(db_item.execute(GET_AVG_SALARY))

    # Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
    print(db_item.execute(GET_VACANCIES_WITH_HIGHER_SALARY))

    # Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например “python”.
    keyword = input("введите ключевое слово для поиска: ")
    print(db_item.get_vacancies_with_keyword(keyword))


if __name__ == '__main__':
    main()
