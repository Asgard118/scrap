import requests
import bs4
import json
from unicodedata import normalize

vacancy_information = []

for page_num in range(0, 9):
    url = f'https://spb.hh.ru/search/vacancy?no_magic=true&L_save_area=true&text=python+django+flask&excluded_text=&area=2&area=1&salary=&currency_code=RUR&experience=doesNotMatter&order_by=relevance&search_period=0&items_on_page=20&page={page_num}'
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    response = requests.get(url, headers=headers)
    page_html = response.text
    page_soup = bs4.BeautifulSoup(page_html, 'lxml')
    vacancy_list_tag = page_soup.find_all('div', class_='vacancy-serp-item__layout')

    for vacancy_tag in vacancy_list_tag:
        vacancy_link = vacancy_tag.find('a', class_='serp-item__title')['href']
        vacancy_name = vacancy_tag.find('a', class_='serp-item__title').text
        company_name_soup = vacancy_tag.find(attrs={'data-qa': 'vacancy-serp__vacancy-employer'})
        company_name = company_name_soup.text if company_name_soup else 'Не указано'
        salary_soup = vacancy_tag.find(attrs={'data-qa': 'vacancy-serp__vacancy-compensation'})
        salary = salary_soup.text if salary_soup else 'Не указано'
        city_soup = vacancy_tag.find(attrs={'data-qa': 'vacancy-serp__vacancy-address'})
        city = city_soup.text.split(',')[0] if city_soup else 'Не указано'

        vacancy_information.append({
            'vacancy_name': normalize('NFKD', vacancy_name),
            'link': normalize('NFKD', vacancy_link),
            'company_name': normalize('NFKD', company_name),
            'salary': normalize('NFKD', salary),
            'city': normalize('NFKD', city)
        })

with open('vacancy_info.json', 'w', encoding="utf-8") as file:
    file.write(json.dumps(vacancy_information, indent=2, ensure_ascii=False))



