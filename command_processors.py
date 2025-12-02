from pymongo import MongoClient

from global_vars import COLL_NAME, DB_NAME, LOCALHOST, PORT


def by_tag(tag):
    collocations = list(MongoClient(LOCALHOST, PORT)[DB_NAME][COLL_NAME].find({'tag': tag}, {'_id': 0, 'tag': 0}))
    if collocations:
        return collocations
    else:
        return ["Aucune collocation trouvée."]
