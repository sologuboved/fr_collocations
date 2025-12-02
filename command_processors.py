from operator import itemgetter
import random

from pymongo import MongoClient

from global_vars import COLL_NAME, DB_NAME, LOCALHOST, PORT


def by_num(num):
    collocations = list(MongoClient(LOCALHOST, PORT)[DB_NAME][COLL_NAME].find(projection={'_id': 0}))
    random.shuffle(collocations)
    return sorted(collocations[:num], key=itemgetter('mot'))


def by_tag(tag):
    collocations = list(MongoClient(LOCALHOST, PORT)[DB_NAME][COLL_NAME].find(
        {'tag': tag},
        {'_id': 0, 'tag': 0},
    ).sort('mot'))
    if collocations:
        return collocations
    else:
        return ["Aucune collocation trouvée."]


def get_tags():
    return sorted(MongoClient(LOCALHOST, PORT)[DB_NAME][COLL_NAME].distinct('tag'))