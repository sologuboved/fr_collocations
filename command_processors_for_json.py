import itertools
from operator import itemgetter
import random

import requests

from config import CITATIONS, COLLOCATIONS, URL_CITATIONS, URL_COLLOCATIONS


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
    dbase = MongoClient(LOCALHOST, PORT)[DB_NAME]
    target = dbase[COLLOCATIONS]
    stats = f"Nombre total : {target.estimated_document_count()} ; y compris {len(target.distinct('tag'))} tags\n\n"
    for item in target.aggregate([
        {"$group": {"_id": "$tag", "count": {"$sum": 1}}},
        {'$sort': {'count': -1}}
    ]):
        stats += f"{item['_id']} : {item['count']}\n"
    target = dbase[CITATIONS]
    stats += f"\nIl y a aussi {target.estimated_document_count()} citations ; {len(target.distinct('auteur'))} auter(s)"
    return stats


if __name__ == '__main__':
    print(get_stats())
