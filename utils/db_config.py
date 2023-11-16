import psycopg2


def create_database(database_name, params):
    """Функция для создания базы данных"""
    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute(f"DROP DATABASE IF EXISTS {database_name}")
    cur.execute(f"CREATE DATABASE {database_name}")
    cur.close()
    conn.close()
    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE employers (
                employer_id INTEGER PRIMARY KEY,
                company_name VARCHAR(100) NOT NULL
                )
        """)
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE vacancies (
                vacancy_id INTEGER PRIMARY KEY,
                vacancy_name VARCHAR,
                salary_from INTEGER,
                salary_to INTEGER,
                requirement TEXT,
                vacancy_url TEXT,
                employer_id INTEGER REFERENCES employers(employer_id)
            )
        """)
    conn.commit()
    conn.close()


def save_employers_to_db(data, database_name, params):
    """Заполняет таблицу employers данными о компаниях"""
    conn = psycopg2.connect(dbname=database_name, **params)
    with conn.cursor() as cur:
        for employer in data:
            query = "INSERT INTO employers (employer_id, company_name) VALUES (%s, %s) ON CONFLICT DO NOTHING"
            cur.execute(query, employer)
    conn.commit()
    conn.close()


def save_vacancies_to_db(data, database_name, params):
    """Заполняет таблицу vacancies данными о вакансиях"""
    conn = psycopg2.connect(dbname=database_name, **params)
    with conn.cursor() as cur:
        for vacancy in data:
            query = ("INSERT INTO vacancies (vacancy_id, vacancy_name, salary_from, salary_to, requirement, "
                     "vacancy_url, employer_id) VALUES ( %s, %s, %s, %s, %s, %s, %s)")
            cur.execute(query, vacancy)
    conn.commit()
    conn.close()
