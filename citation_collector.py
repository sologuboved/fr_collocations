from collections import defaultdict
import time

from bs4 import BeautifulSoup
from pymongo import MongoClient
import requests

from config import CITATIONS, DB_NAME, LOCALHOST, PORT
from helpers import dump_utf_json, load_utf_json


def collect(url, auteur):
    print(auteur + '...')
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
    return citations


def upload(citations, drop):
    target = MongoClient(LOCALHOST, PORT)[DB_NAME][CITATIONS]
    if drop:
        target.drop()
    print(f"Initialement, {target.estimated_document_count()} entrées")
    target.insert_many(citations)
    print(f"Enfin, {target.estimated_document_count()} entrées")


def download(citations, drop):
    contents = defaultdict(list)
    if not drop:
        contents.update(load_utf_json('citations.json'))
    for citation in citations:
        contents[citation['auteur']].append(citation)
    dump_utf_json(contents, 'citations.json')


def main(to_db, drop):
    citations = list()
    for url, auteur in (
            (
                    'http://evene.lefigaro.fr/citations/blaise-pascal?page=',
                    "Blaise Pascal",
            ),
            (
                    'http://evene.lefigaro.fr/citations/francois-de-la-rochefoucauld?page=',
                    "François de La Rochefoucauld",
            ),
            (
                    'http://evene.lefigaro.fr/citations/montesquieu?page=',
                    "De Montesquieu",
            ),
            (
                    'http://evene.lefigaro.fr/citations/montaigne?page=',
                    "Michel de Montaigne",
            ),
    ):
        for collected in collect(url, auteur):
            citations.extend(collected)
    if to_db:
        upload(citations, drop)
    else:
        download(citations, drop)


if __name__ == '__main__':
    main(to_db=False, drop=True)
