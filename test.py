from requests import get
from fake_headers import Headers
from bs4 import BeautifulSoup as bs
from pprint import pprint
import json
import re


URL = 'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2'
headers = Headers(browser='opera', os='mac').generate()
html = get(url=URL, headers=headers).text
    

soup = bs(html, features='lxml')
vacancys_list = soup.find_all(class_='vacancy-serp-item__layout')
result = []
for vacancy in vacancys_list:
    link = vacancy.find('a')['href']
    wage = vacancy.find(name='span', class_='bloko-header-section-2')
    if wage != None:
        wage = ' '.join(wage.text.split())
    else:
        wage = 'Зароботная плата не указана'
    company = vacancy.find('a', class_='bloko-link bloko-link_kind-tertiary').text
    city = vacancy.find('div', {'data-qa':'vacancy-serp__vacancy-address'}).text
    vacancy_html = get(link, headers=headers).text
    vacancy_soup = bs(vacancy_html, features='lxml')
    vacancy_desc_tag = vacancy_soup.find('div', class_ = 'bloko-columns-row')
    vacancy_desc = vacancy_desc_tag.text
    if 'flask' in vacancy_desc.lower() and 'django' in vacancy_desc.lower():
        result.append({
        'Ссылка': link,
        'Зарплата': wage,
        'Компания': company,
        'Город': city})

with open('vacancy.json', 'w', encoding='utf-8') as file:
    json.dump(result, file, indent=4)

pprint(result)