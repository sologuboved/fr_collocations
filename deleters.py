from pymongo import MongoClient

from global_vars import COLL_NAME, DB_NAME, LOCALHOST, PORT


def del_by_tag(tag):
    print(f"Del {tag} from {DB_NAME}.{COLL_NAME}...")
    target = MongoClient(LOCALHOST, PORT)[DB_NAME][COLL_NAME]
    print(f"Initially, {target.estimated_document_count()} entries")
    target.delete_many({'tag': tag})
    print(f"Finally, {target.estimated_document_count()} entries")


if __name__ == '__main__':
    del_by_tag('phrases')
