import itertools
from operator import itemgetter
import random

import requests

from config import URL_CITATIONS, URL_COLLOCATIONS


def order(seq, by='mot'):
    return sorted(seq, key=itemgetter(by))


def get_data(url=URL_COLLOCATIONS):
    return requests.get(url).json()


def by_random(size):
    data = get_data()
    if size:
        tags = list(data.keys())
        sample = list()
        for _ in range(size):
            tag = random.choice(tags)
            sample.append(random.choice(data[tag]) | {'tag': tag})
        return order(sample)
    else:
        return order([random.choice(val) | {'tag': tag} for tag, val in data.items()], by='tag')


def by_tag(tag):
    collocations = list()
    try:
        data = get_data()[tag]
    except KeyError:
        pass
    else:
        for collocation in data:
            collocations.append(collocation)
    if collocations:
        return order(collocations)
    else:
        return ["Aucune collocation trouvée."]


def get_tags():
    return sorted(get_data().keys())


def get_all():
    tags_and_collocations = list()
    data = get_data()
    for tag, val in sorted(data.items()):
        collocations = list()
        for entry in val:
            collocations.append(entry)
        tags_and_collocations.append((tag, order(collocations)))
    return tags_and_collocations


def get_citation():
    data = get_data(url=URL_CITATIONS)
    auteur = random.choice(list(data.keys()))
    citation = random.choice(data[auteur])
    livre = citation.pop('œuvre')
    citation = f"{citation['cit']}\n\n{auteur}"
    if livre:
        citation += f" - {livre}"
    return citation


def get_stats():
    stats = ''
    for url, label in (
        (URL_COLLOCATIONS, "Nombre total : {} ; y compris {} tag(s):\n\n"),
        (URL_CITATIONS, "\nIl y a aussi {} citations ; {} auteur(s):\n\n"),
    ):
        data = get_data(url=url)
        num_keys = len(data.keys())
        num_entries = len(list(itertools.chain.from_iterable(data.values())))
        stats += label.format(num_keys, num_entries)
        for key, val in data.items():
            stats += f"{key} : {len(val)}\n"
    return stats


if __name__ == '__main__':
    print(get_stats())
