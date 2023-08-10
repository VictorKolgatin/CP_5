CREATE_TABLE_EMP = """
                    TABLE employers
                    (
                        employer_id   int PRIMARY KEY,
                        employer_name varchar(255),
                        employer_url  varchar(255),
                        open_vacancy  int
                    )"""

CREATE_TABLE_VAC = """
                   CREATE TABLE vacancies
                   (
                       area         varchar(255),
                       name_vacancy varchar(255),
                       employer     varchar(255),
                       url_vac      varchar(255),
                       salary_from  int,
                       salary_to    int
                   )"""

# Получает список всех компаний и количество вакансий у каждой компании.
GET_COMPANIES_AND_VACANCIES_COUNT = """
                                    SELECT employer, COUNT(*)
                                    FROM vacancies
                                    GROUP BY employer
                                    ORDER BY COUNT(*) DESC
                                    """

# Получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.
GET_ALL_VACANCIES = """
                    SELECT employer, name_vacancy, salary_from, salary_to, currency, url_vac
                    FROM vacancies
                    """

# Получает среднюю зарплату по вакансиям.
GET_AVG_SALARY = """
                SELECT round(AVG(salary_from)) as от,
                       (SELECT round(AVG(salary_to)) as до
                        FROM vacancies
                        WHERE salary_to <> 0)
                FROM vacancies
                WHERE salary_from <> 0
                """

# Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
GET_VACANCIES_WITH_HIGHER_SALARY = """
                                SELECT name_vacancy, employer, salary_from, url_vac
                                FROM vacancies
                                WHERE salary_from >= (SELECT AVG(salary_from) FROM vacancies)
                                ORDER BY employer
                                """

