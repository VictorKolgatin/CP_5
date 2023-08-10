import requests
from config import employers_id


class HeadHunterAPI:
    """
    Класс для работы с API сервиса hh.ru
    """

    def __init__(self):
        self.employers_id = employers_id

    def get_employers(self):
        """
        Метод класса HeadHunterAPI, для получения интересующих работодателй по их id.
        """
        employers_list = []
        for i in self.employers_id.values():
            response = requests.get(f'https://api.hh.ru/employers/{i}').json()

            employers = {'emp_id': response['id'],
                         'emp_name': response['name'],
                         'emp_url': response['alternate_url'],
                         'open_vacancy': response['open_vacancies']}

            employers_list.append(employers)
        return employers_list

    def get_vacancies_and_format(self):
        """
        Получает вакансии по HH API по id работодателя.
        Форматируем список вакансий к удобному виду.
        """
        vac_emp = []
        for i in self.employers_id.values():
            vacancy = requests.get(f"https://api.hh.ru/vacancies?employer_id={i}").json()['items']

            for vacancy in vacancy:
                area = vacancy['area']['name']
                name = vacancy['name']
                employer = vacancy['employer']['name']
                url_vacancy = vacancy['alternate_url']

                salary = vacancy['salary']
                if not salary:
                    salary_from = 0
                    salary_to = 0
                    currency = ''
                else:
                    salary_from = vacancy['salary']['from'] if vacancy['salary']['from'] else 0
                    salary_to = vacancy['salary']['to'] if vacancy['salary']['to'] else 0
                    currency = vacancy['salary']['currency'] if vacancy['salary'][
                        'currency'] else 'Currency not specified'

                vac_emp.append({'area': area,
                                'name': name,
                                'employer': employer,
                                'url': url_vacancy,
                                'salary_from': salary_from,
                                'salary_to': salary_to,
                                'currency': currency
                                })

        return vac_emp
