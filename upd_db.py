from pymongo import MongoClient

from global_vars import COLLOCATIONS, DB_NAME, LOCALHOST, PORT
from helpers import read_csv


class Entries:
    def __init__(self):
        self.entries = list()

    def __iadd__(self, other):
        self.entries.append(dict(zip(('mot', 'trad', 'tag'), other)))
        return self


def add_tag(mot, trad, tag, coll_name=COLLOCATIONS):
    print(f"Adding {tag}...")
    MongoClient(LOCALHOST, PORT)[DB_NAME][coll_name].insert_one({'mot': mot, 'trad': trad, tag: 'tag'})
    print('...done')


def by_tag(tag, drop=False):
    print(f"{tag} -> {DB_NAME}.{COLLOCATIONS}")
    entries = Entries()
    with open('mots_temp.txt') as handler:
        for line in handler.readlines():
            if not line.strip():
                continue
            line = line.split('~')
            try:
                mot, trad = map(str.strip, line)
            except ValueError:
                mot = line[0].strip()
                trad = None
            entries += (mot, trad, tag)
            # print(mot)
    target = MongoClient(LOCALHOST, PORT)[DB_NAME][COLLOCATIONS]
    if drop:
        target.drop()
    print(f"Initially, {target.estimated_document_count()} entries")
    target.insert_many(entries.entries)
    print(f"Finally, {target.estimated_document_count()} entries")


def from_csv(coll_name=COLLOCATIONS, drop=False):
    print(f"mots_temp.csv -> {DB_NAME}.{COLLOCATIONS}")
    target = MongoClient(LOCALHOST, PORT)[DB_NAME][coll_name]
    print(f"Initially, {target.estimated_document_count()} entries")
    if drop:
        target.drop()
    tags = target.distinct('tag')
    entries = list()
    for row in read_csv('mots_temp.csv', as_dict=True):
        mot = row['mot'].strip()
        trad = row['trad'].strip()
        tag = row['tag'].strip()
        if target.find_one({'mot': mot}):
            print(f"'{mot}' est déjà présent ; on l'omet")
            continue
        elif tag not in tags:
            print(f"'{tag}' n'existe pas ; on l;'omet (row {mot},{row['trad']},{tag})")
            continue
        else:
            row['trad'] = trad or None
            row['tag'] = tag
            entries.append(row)
    if entries:
        target.insert_many(entries)
    print(f"Finally, {target.estimated_document_count()} entries")


if __name__ == '__main__':
    # by_tag('phrases')
    # add_tag(mot='', trad=None, tag='')
    from_csv(
        # coll_name=COLLOCATIONS + '_test',
    )
