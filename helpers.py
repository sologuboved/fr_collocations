from pymongo import MongoClient

from global_vars import COLL_NAME, DB_NAME, LOCALHOST, PORT


def to_txt(filename='collocations.txt'):
    print(f"Writing {filename}...")
    tag_count = mot_count = 0
    text = str()
    target = MongoClient(LOCALHOST, PORT)[DB_NAME][COLL_NAME]
    for tag in sorted(target.distinct('tag')):
        tag_count += 1
        text += tag.upper() + '\n'
        for entry in target.find({'tag': tag}).sort('mot', 1):
            try:
                text += " ~ ".join((entry['mot'], entry['trad'])) + '\n'
            except TypeError:
                text += entry['mot'] + '\n'
            mot_count += 1
        text += '\n'
    text = text[:-1]
    with open(filename, 'w') as handler:
        handler.write(text)
    print(f"Wrote {tag_count} tags, {mot_count} collocations")


def del_by_tag(tag):
    print(f"Del {tag} from {DB_NAME}.{COLL_NAME}...")
    target = MongoClient(LOCALHOST, PORT)[DB_NAME][COLL_NAME]
    print(f"Initially, {target.estimated_document_count()} entries")
    target.delete_many({'tag': tag})
    print(f"Finally, {target.estimated_document_count()} entries")


if __name__ == '__main__':
    to_txt()
