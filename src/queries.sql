CREATE TABLE employers
(
    employer_id   int PRIMARY KEY,
    employer_name varchar(255),
    employer_url  varchar(255),
    open_vacancy  int
);

CREATE TABLE vacancies
(
    area         varchar(255),
    name_vacancy varchar(255),
    employer     varchar(255),
    url_vac      varchar(255),
    salary_from  int,
    salary_to    int,
    currency     varchar(255),
);

SELECT employer, COUNT(*)
FROM vacancies
GROUP BY employer
ORDER BY COUNT(*) DESC;

SELECT employer, name_vacancy, salary_from, selary_to, currency, url_vac
FROM vacancies;

SELECT round(AVG(salary_from)) as от,
       (SELECT round(AVG(salary_to)) as до
        FROM vacancies
        WHERE salary_to <> 0)
FROM vacancies
WHERE salary_from <> 0;

SELECT name_vacancy, employer, salary_from, url_vac
FROM vacancies
WHERE salary_from >= (SELECT AVG(salary_from) FROM vacancies)
ORDER BY employer;

SELECT name_vacancy, employer, url_vac
FROM vacancies
WHERE lower(name_vacancy) LIKE %keyword%


