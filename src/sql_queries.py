GET_VACANCIES_WITH_HIGHER_SALARY = """
SELECT name_vacancy, employer, salary_from, url_vac
                        FROM vacancies
                        WHERE salary_from >= (SELECT AVG(salary_from) FROM vacancies)
                        ORDER BY employer
"""





