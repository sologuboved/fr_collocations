from operator import itemgetter
import random

from pymongo import MongoClient

from global_vars import CITATIONS, COLLOCATIONS, DB_NAME, LOCALHOST, PORT


def by_num(num):
    collocations = list(MongoClient(LOCALHOST, PORT)[DB_NAME][COLLOCATIONS].find(projection={'_id': 0}))
    random.shuffle(collocations)
    return sorted(collocations[:num], key=itemgetter('mot'))


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
    stats += f"\nIl y a aussi {target.estimated_document_count()} citations ; {len(target.distinct('auteur'))} auters"
    return stats


if __name__ == '__main__':
    print(get_stats())
