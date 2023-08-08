import psycopg2
import csv

from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2 import Error

from config import host, database, user, password


class DBManager:
    """
    Класс для работы с БД.
    """

    def __init__(self, host=host, database=database, user=user, password=password):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.conn = None

    def conn_db(self):
        """
        Подключаемся к БД.
        """
        self.conn = psycopg2.connect(
            host=self.host,
            database=self.database,
            user=self.user,
            password=self.password
        )

        return self.conn

    def create_db(self, name_db):
        try:
            # Подключение к существующей базе данных
            conn = psycopg2.connect(user=self.user,
                                    password=self.password,
                                    host=self.host,
                                    port="5432")
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            # Курсор для выполнения операций с базой данных
            cursor = conn.cursor()
            sql_create_database = f'create database {name_db}'
            cursor.execute(sql_create_database)
        except (Exception, Error) as error:
            print("Ошибка при работе с PostgreSQL", error)
        finally:
            if conn:
                cursor.close()
                conn.close()
                print("Соединение с PostgreSQL закрыто")


    def create_tab_emp(self):
        conn = self.conn_db()
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE employers
                (
                    employer_id int PRIMARY KEY,
                    employer_name varchar(255),
                    employer_url varchar(255),
                    open_vacancy int
                )
            """)
        conn.commit()
        conn.close()

    def create_tab_vac(self):
        conn = self.conn_db()
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE vacancies
                (
                    area varchar (255),
                    name_vacancy varchar (255),
                    employer varchar (255),
                    url_vac varchar (255),
                    salary_from int,
                    salary_to int,
                    currency varchar (255),
                )
            """)
        conn.commit()
        conn.close()

    def insert_emp(self):
        """
        Заполнение данными employers
        """
        file_employers = '/home/vk/Рабочий стол/Курс SkyPro/5.SQL/CP_5/src/employers.csv'
        conn = self.conn_db()
        try:
            with conn:
                with conn.cursor() as cur:
                    with open(file_employers) as csvfile:
                        readers = csv.DictReader(csvfile)
                        for reader in readers:
                            cur.execute("INSERT INTO employers VALUES (%s, %s, %s, %s)",
                                        (reader['emp_id'], reader['emp_name'], reader['emp_url'],
                                         reader['open_vacancy']))
        finally:
            conn.close()

    def insert_vac(self):
        """
        Заполнение данными employers
        """
        file_vacancy = '/home/vk/Рабочий стол/Курс SkyPro/5.SQL/CP_5/src/vacancies.csv'
        conn = self.conn_db()
        try:
            with conn:
                with conn.cursor() as cur:
                    with open(file_vacancy) as csvfile:
                        readers = csv.DictReader(csvfile)
                        for reader in readers:
                            cur.execute("INSERT INTO vacancies VALUES (%s, %s, %s, %s, %s, %s, %s)",
                                        (reader['area'], reader['name'], reader['employer'],
                                         reader['url'], reader['salary_from'], reader['salary_to'],
                                         reader['currency']))
        finally:
            conn.close()

    def get_companies_and_vacancies_count(self):
        """
        Получает список всех компаний и количество вакансий у каждой компании.
        """
        conn = self.conn_db()
        with conn.cursor() as cur:
            cur.execute("""
                SELECT employer, COUNT(*)
                FROM vacancies
                GROUP BY employer
                ORDER BY COUNT(*) DESC 
            """)
            result = cur.fetchall()
        conn.close()
        return result

    def get_all_vacancies(self):
        """
        Получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию.
        """
        conn = self.conn_db()
        with conn.cursor() as cur:
            cur.execute("""
                        SELECT employer, name_vacancy, salary_from, selary_to, currency, url_vac
                        FROM vacancies 
                        """)
            result = cur.fetchall()
        conn.close()
        return result

    def get_avg_salary(self):
        """
        Получает среднюю зарплату по вакансиям.
        """
        conn = self.conn_db()
        with conn.cursor() as cur:
            cur.execute("""
                        SELECT round(AVG(salary_from)) as от, 
                        (SELECT round(AVG(salary_to)) as до 
                        FROM vacancies WHERE salary_to <> 0)
                        FROM vacancies 
                        WHERE salary_from <>0""")
            result = cur.fetchall()
        conn.close()
        return result

    def get_vacancies_with_higher_salary(self):
        """
        Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
        """
        conn = self.conn_db()
        with conn.cursor() as cur:
            cur.execute("""
                        SELECT name_vacancy, employer, salary_from, url_vac
                        FROM vacancies
                        WHERE salary_from >= (SELECT AVG(salary_from) FROM vacancies)
                        ORDER BY employer""")
            result = cur.fetchall()
        conn.close()
        return result

    def get_vacancies_with_keyword(self, keyword):
        """
        Получает список всех вакансий, в названии которых содержатся переданные в метод слова,
        например “python”.
        """
        conn = self.conn_db()
        kw = keyword.lower()
        with conn.cursor() as cur:
            cur.execute("""
                        SELECT name_vacancy, employer, url_vac
                        FROM vacancies
                        WHERE lower(name_vacancy) LIKE '%{kw}%'
                        """)
            result = cur.ftchall()
        conn.close()
        return result

