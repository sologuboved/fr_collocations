import time

from bs4 import BeautifulSoup
from pymongo import MongoClient
import requests

from global_vars import CITATIONS, DB_NAME, LOCALHOST, PORT


def collect_quotes(url, auteur, drop):
    citations = list()
    page = 0
    is_off = True
    while True:
        time.sleep(1)
        page += 1
        print(page)
        for article in BeautifulSoup(requests.get(url + str(page)).content, 'lxml').find_all('article')[1:]:
            try:
                livre = article.find('div', {'class': 'figsco__fake__col-9'}).text.rsplit('/', 1)[1].strip()
            except IndexError:
                livre = None
            citations.append({
                'cit': article.find('div', {'class': 'figsco__quote__text'}).text.strip(),
                'œuvre': livre,
                'auteur': auteur,
            })
            is_off = False
        if is_off:
            break
        is_off = True
    target = MongoClient(LOCALHOST, PORT)[DB_NAME][CITATIONS]
    if drop:
        target.drop()
    print(f"Initialement, {target.estimated_document_count()} entrées")
    target.insert_many(citations)
    print(f"Enfin, {target.estimated_document_count()} entrées")


if __name__ == '__main__':
    # collect_quotes(
    #     url='http://evene.lefigaro.fr/citations/blaise-pascal?page=',
    #     auteur="Blaise Pascal",
    #     drop=True,
    # )
    # collect_quotes(
    #     url='http://evene.lefigaro.fr/citations/francois-de-la-rochefoucauld?page=',
    #     auteur="François de La Rochefoucauld",
    #     drop=False,
    # )
    # collect_quotes(
    #     url='http://evene.lefigaro.fr/citations/montesquieu?page=',
    #     auteur="De Montesquieu",
    #     drop=False,
    # )
    collect_quotes(
        url='http://evene.lefigaro.fr/citations/montaigne?page=',
        auteur="Michel de Montaigne",
        drop=False,
    )
