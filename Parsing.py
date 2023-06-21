import requests
from bs4 import BeautifulSoup

def get_links_by_class(url, class_name):
    response = requests.get(url)
    if response.status_code != 200:
        print("Ошибка при получении страницы")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    elements = soup.find_all(class_=class_name)
    links = []
    for element in elements:
        link = element.get('href')
        if link:
            links.append(link)
    return links


url = 'https://student39.ru/news/'
class_name = 'newsItem'

links = get_links_by_class(url, class_name)
