import itertools
from operator import itemgetter
import random

import requests

from config import CITATIONS, COLLOCATIONS, URL


def order(seq):
    return sorted(seq, key=itemgetter('mot'))


def get_data():
    return requests.get(URL).json()


def by_random(size):
    data = get_data()
    if size:
        return order(random.sample([collocation['mot'] for val in data.values() for collocation in val], size))
    else:
        return order([random.choice(val) for val in data.values()])


def by_tag(tag):
    collocations = list(MongoClient(LOCALHOST, PORT)[DB_NAME][COLLOCATIONS].find(
        {'tag': tag},
        {'_id': 0, 'tag': 0},
    ).sort('mot'))
    if collocations:
        return collocations
    else:
        return ["Aucune collocation trouvée."]


def get_tags():
    return sorted(MongoClient(LOCALHOST, PORT)[DB_NAME][COLLOCATIONS].distinct('tag'))


def get_all():
    tags_and_collocations = list()
    target = MongoClient(LOCALHOST, PORT)[DB_NAME][COLLOCATIONS]
    for tag in sorted(target.distinct('tag')):
        tags_and_collocations.append((tag, list(target.find({'tag': tag}, {'_id': 0, 'tag': 0}).sort('mot'))))
    return tags_and_collocations


def get_citation():
    citation = next(MongoClient(LOCALHOST, PORT)[DB_NAME][CITATIONS].aggregate([{'$sample': {'size': 1}}]))
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
