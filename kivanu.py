from os import error
from bs4 import BeautifulSoup
import requests
import csv 

CSV = 'kivano_nout.csv'
HOST = 'https://www.kivano.kg'
URL = 'https://www.kivano.kg/noutbuki'
HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
  'User-Agent : Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:94.0) Gecko/20100101 Firefox/94.0'
}

def get_html(url,params = ''):
    r = requests.get(url,headers= HEADERS,params=params)
    return r

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.findAll('div', class_ = 'item product_listbox oh') #dva raza klikaem po mishke
    new_list =[]
    for item in items:
        new_list.append({
            'title': item.find('div', class_='product_text pull-left').find('div', class_='listbox_title oh').find('a').get_text(strip=True)
        })
    return new_list

    return new_list

def save(items,path):
    with open(path,'a') as file:
        writer = csv.writer(file,delimiter=';')
        writer.writerow(['Название'])
        for item in items:
            writer.writerow([item['title']])

def parser():
    PAGINATION =input('Ведите количество страниц:  ')
    PAGINATION =int(PAGINATION.strip())
    html = get_html(URL)
    if html.status_code ==200:
        new_list = []
        for page in range(1,PAGINATION):
            print(f'Страница {page} готова!')
            html = get_html(URL,params={'page':page})
            new_list.extend(get_content(html.text))
        save(new_list,CSV)
        print('Парсинг готов!')
    else:
        print('error')
parser()