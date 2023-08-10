import psycopg2
import csv

from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2 import Error

from config import HOST, DATABASE, USER, PASSWORD, PORT


class DBManager:
    """
    Класс для работы с БД.
    """

    def __init__(self, host=HOST, database=DATABASE, user=USER, password=PASSWORD, port=PORT):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.conn = None
        self.port = port

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
        conn = None
        cursor = None
        try:
            # Подключение к существующей базе данных
            conn = psycopg2.connect(user=self.user,
                                    password=self.password,
                                    host=self.host,
                                    port=self.port)
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

    def insert_emp(self):
        """
        Заполнение данными employers
        """
        file_employers = 'employers.csv'
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
        file_vacancy = 'vacancies.csv'
        conn = self.conn_db()
        try:
            with conn:
                with conn.cursor() as cur:
                    with open(file_vacancy) as csvfile:
                        readers = csv.DictReader(csvfile)
                        for reader in readers:
                            cur.execute("INSERT INTO vacancies VALUES (%s, %s, %s, %s, %s, %s)",
                                        (reader['area'], reader['name'], reader['employer'],
                                         reader['url'], reader['salary_from'], reader['salary_to']))
        finally:
            conn.close()

    def execute(self, sql_queries):
        """
        Выполнение sql запросов, файл queries.py
        """
        conn = self.conn_db()
        with conn.cursor() as cur:
            cur.execute(sql_queries)

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
            cur.execute(f"""
                        SELECT name_vacancy, employer, url_vac
                        FROM vacancies
                        WHERE lower(name_vacancy) LIKE '%{kw}%'
                        """)
            result = cur.ftchall()
        conn.close()
        return result
