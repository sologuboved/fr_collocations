from pymongo import MongoClient

from global_vars import COLLOCATIONS, DB_NAME, LOCALHOST, PORT
from helpers import upsert_mongo_entry


def empty_str_to_null():
    target = MongoClient(LOCALHOST, PORT)[DB_NAME][COLLOCATIONS]
    count = 0
    for entry in target.find():
        if entry['trad'] == '':
            entry['trad'] = None
            upsert_mongo_entry(target, entry)
            count += 1
    print(count)


if __name__ == '__main__':
    empty_str_to_null()
