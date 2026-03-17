from pymongo import MongoClient

from global_vars import COLLOCATIONS, DB_NAME, LOCALHOST, PORT
from helpers import read_csv, upsert_mongo_entry
import write


def edit_tags(email=False):
    coll = MongoClient(LOCALHOST, PORT)[DB_NAME][COLLOCATIONS]
    count = 0
    for mot, tag in read_csv('edits.csv', as_dict=False):
        match = coll.find_one({'mot': mot})
        if match is None:
            print(f"{mot} -> {tag}: 404")
            continue
        match['tag'] = tag
        upsert_mongo_entry(coll, match)
        count += 1
    print('Modified', count)
    write.to_csv()
    write.to_txt()
    if email:
        write.to_email()


if __name__ == '__main__':
    edit_tags(
        # email=True,
    )
