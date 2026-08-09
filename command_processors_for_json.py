import itertools
from operator import itemgetter
import random

import requests

from config import URL_CITATIONS, URL_COLLOCATIONS


def order(seq):
    return sorted(seq, key=itemgetter('mot'))


def get_data(url=URL_COLLOCATIONS):
    return requests.get(url).json()


def by_random(size):
    data = get_data()
    if size:
        return order(random.sample([collocation['mot'] for val in data.values() for collocation in val], size))
    else:
        return order([random.choice(val) for val in data.values()])


def by_tag(tag):
    collocations = list()
    try:
        data = get_data()[tag]
    except KeyError:
        pass
    else:
        for collocation in data:
            collocations.pop(tag)
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
            entry.pop(tag)
            collocations.append(entry)
        tags_and_collocations.append((tag, order(collocations)))
    return tags_and_collocations


def get_citation():
    citation = random.choice(get_data(url=URL_CITATIONS))
    livre = citation.pop('œuvre')
    citation = f"{citation['cit']}\n\n{citation['auteur']}"
    if livre:
        citation += f" - {livre}"
    return citation


def get_stats():
    data = get_data()
    num_tags = len(data.keys())
    num_entries = len(list(itertools.chain.from_iterable(data.values())))
    stats = f"Nombre total : {num_entries} ; y compris {num_tags} tags\n\n"
    for tag, val in data.items:
        stats += f"{tag} : {len(val)}\n"
    data = get_data(url=URL_CITATIONS)
    stats += f"\nIl y a aussi {len(data)} citations ; {len({entry['auteur'] for entry in data})} auter(s)"
    return stats


if __name__ == '__main__':
    print(get_stats())
