from collections import defaultdict

from pymongo import MongoClient

from config import CITATIONS, DB_NAME, LOCALHOST, PORT
from helpers import dump_utf_json, load_utf_json, read_csv


def collocations_csv_to_json():
    collocations = defaultdict(list)
    for row in read_csv('collocations.csv', as_dict=True):
        if not row['trad']:
            row['trad'] = None
        collocations[row['tag']].append(row)
    dump_utf_json(collocations, 'collocations.json')


def download_citations():
    dump_utf_json(
        list(MongoClient(LOCALHOST, PORT)[DB_NAME][CITATIONS].find(projection={'_id': 0})),
        'citations.json',
    )


def remove_individual_tags():
    collocations = dict()
    for tag, val_with_individual_tags in load_utf_json('collocations.json').items():
        val = list()
        for entry in val_with_individual_tags:
            entry.pop('tag')
            val.append(entry)
        collocations[tag] = val
    dump_utf_json(collocations, 'collocations.json')


if __name__ == '__main__':
    remove_individual_tags()
