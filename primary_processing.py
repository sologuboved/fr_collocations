from pymongo import MongoClient

from global_vars import COLL_NAME, DB_NAME, LOCALHOST, PORT


class Entries:
    def __init__(self):
        self.entries = list()

    def __iadd__(self, other):
        self.entries.append(dict(zip(('mot', 'trad', 'tag'), other)))
        return self


def by_tag(tag, drop=False):
    print(f"{tag} -> {DB_NAME}.{COLL_NAME}")
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
    target = MongoClient(LOCALHOST, PORT)[DB_NAME][COLL_NAME]
    if drop:
        target.drop()
    print(f"Initially, {target.estimated_document_count()} entries")
    target.insert_many(entries.entries)
    print(f"Finally, {target.estimated_document_count()} entries")


if __name__ == '__main__':
    by_tag('phrases')
