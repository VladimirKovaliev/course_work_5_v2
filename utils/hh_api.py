import requests


def get_company_data(companies_id: dict):
    """Получает данные о компаниях по АПИ HH"""
    companies_data = []
    data = []
    for company_id in companies_id:
        params = {'per_page': 50}
        hh_url_companies = f'https://api.hh.ru/employers/{company_id}'
        response = requests.get(hh_url_companies, params=params)
        items = response.json()
        data.append(items)
        for item in data:
            company_id = item['id']
            company_name = item['name']
            companies_data.append([company_id, company_name])
    return companies_data

def get_vacancies_hh(vacancies):
    """Получает данные по вакансиям"""
    vacancies_data = []
    for employer_id in vacancies:
        params = {'per_page': 50}
        hh_url_vacancies = f'https://api.hh.ru/vacancies?employer_id={employer_id}'
        response = requests.get(hh_url_vacancies, params=params)
        items = response.json()['items']
        for item in items:
            salary = item['salary']
            vacancy_id = item['id']
            vacancy_name = item['name']
            salary_from = 0 if salary is None or salary['from'] is None else salary['from']
            salary_to = 0 if salary is None or salary['to'] is None else salary['to']
            requrement = item['snippet']['requirement']
            vacancy_url = item['alternate_url']
            employer_id = item['employer']['id']
            vacancies_data.append([vacancy_id, vacancy_name, salary_from, salary_to, requrement, vacancy_url, employer_id])
            return vacancies_data

