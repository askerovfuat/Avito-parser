import requests
from bs4 import BeautifulSoup
import csv

""" План:
1. Вычислить кол-во страниц
2. Сформировать список url'ов на страницы выдачи
3. Собрать данные """


def get_html(url):
    r = requests.get(url)
    return r.text


def get_total_pages(html):
    soup = BeautifulSoup(html, 'lxml')
    pages = soup.find('div', class_='pagination-pages').find_all('a',
                                                                 class_='pagination-page')[-1].get('href')
    total_pages = pages.split('=')[1].split('&')[0]
    return int(total_pages)


def write_csv(data):
    with open('avito.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow((data['title'],
                         data['price'],
                         data['area'],
                         data['url']))


def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')

    ads = soup.find('div', class_='items-items-38oUm').find_all('div',
                                                                class_='iva-item-body-NPl6W')

    for ad in ads:
        try:
            title = ' '.join(ad.find('a').get('title').split()[:-2])
        except:
            title = ''

        try:
            url = 'https://www.avito.ru' + ad.find('a').get('href')
        except:
            url = ''

        try:
            price = ad.find(itemprop="price").get("content")
        except:
            price = ''

        try:
            area = ad.find(
                'div', class_='geo-georeferences-3or5Q text-text-1PdBw text-size-s-1PUdo').find('span').text
        except:
            area = ''

        data = {'title': title, 'price': price, 'area': area, 'url': url}

        write_csv(data)


def main():
    url = 'https://www.avito.ru/moskva/telefony?p=1&q=iphone'
    base_url = 'https://www.avito.ru/moskva/telefony?'
    page_part = 'p='
    query_part = 'q=samsung'

    total_pages = get_total_pages(get_html(url))

    for i in range(1, 3):
        url_gen = base_url + page_part + str(i) + query_part
        html = get_html(url_gen)
        get_page_data(html)


if __name__ == '__main__':
    main()
