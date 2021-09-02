import requests
from bs4 import BeautifulSoup

URL_INFO = 'https://vk-top-groups.ru/'


def get_most_popular_groups():
    """
    Вытаскивает самые популярные группы в вк с сайта аналитики
    такой финт ушами нужен для обхода ограничения при поиске по пользователям в 1000
    в группах можно искать без ограничений
    """

    html = requests.get(URL_INFO).text
    html_tree = BeautifulSoup(html, 'html.parser')

    group_table = html_tree.find('table').find('tbody')
    raw_rows = group_table.find_all('tr')

    rows = [row for row in raw_rows if row.find('td', class_='specifictd')]
    groups_name = [row.find('td', class_='specifictd').text for row in rows]
    groups_name = [name[0:-3] for name in groups_name]

    return groups_name
