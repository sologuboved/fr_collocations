import time

from bs4 import BeautifulSoup
from pymongo import MongoClient
import requests

from global_vars import CITATIONS, DB_NAME, LOCALHOST, PORT


def collect_quotes():
    citations = list()
    page = 0
    is_off = True
    while True:
        time.sleep(1)
        page += 1
        print(page)
        for article in BeautifulSoup(
                requests.get(f'http://evene.lefigaro.fr/citations/blaise-pascal?page={page}').content,
                'lxml',
        ).find_all('article')[1:]:
            try:
                livre = article.find('div', {'class': 'figsco__fake__col-9'}).text.rsplit('/', 1)[1].strip()
            except IndexError:
                livre = None
            citations.append({
                'cit': article.find('div', {'class': 'figsco__quote__text'}).text.strip(),
                'livre': livre,
                'auteur': "Blaise Pascal",
            })
            is_off = False
        if is_off:
            break
        is_off = True
    target = MongoClient(LOCALHOST, PORT)[DB_NAME][CITATIONS]
    print(f"Initialement, {target.estimated_document_count()} entrées")
    target.insert_many(citations)
    print(f"Enfin, {target.estimated_document_count()} entrées")


if __name__ == '__main__':
    collect_quotes()
