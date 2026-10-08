import csv
import json
import os


class SpreadsheetWriter:
    def __init__(self, filename, headers=None):
        print(f"Downloading {filename}...")
        self._filename = filename
        self._headers = headers
        self._as_dict = ...
        self._count = 0
        self._first_row = None
        self._writer = self.writer()
        next(self._writer)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def bulk(self, bulk):
        for row in bulk:
            self.write(row)

    def write(self, row):
        self._count += 1
        self._writer.send(row)

    def close(self):
        self._writer.close()
        print(f"Total: {self._count} row(s)")

    def start(self, first_row):
        self._first_row = first_row
        self._as_dict = isinstance(self._first_row, dict)
        if self._as_dict and not self._headers:
            self._headers = sorted(self._first_row.keys())

    def writer(self):
        raise NotImplemented


class CsvWriter(SpreadsheetWriter):
    def writer(self):
        self.start((yield))
        with open(self._filename, 'w', newline='', encoding='utf-8') as handler:
            if self._as_dict:
                writer = csv.DictWriter(handler, fieldnames=self._headers, restval=None)
                writer.writeheader()
            else:
                writer = csv.writer(handler)
                if self._headers:
                    writer.writerow(self._headers)
            writer.writerow(self._first_row)
            while True:
                writer.writerow((yield))


def get_base_dir():
    return os.path.dirname(os.path.abspath(__file__))


def get_abs_path(fname, base_dir=None):
    if base_dir is None:
        base_dir = get_base_dir()
    return os.path.join(base_dir, fname)


def read_csv(csv_fname, as_dict, delimiter=',', has_headers=True):
    with open(csv_fname, newline=str()) as handler:
        if as_dict:
            assert has_headers, "Doesn't have headers"
            for row in csv.DictReader(handler, delimiter=delimiter):
                yield row
        else:
            reader = csv.reader(handler, delimiter=delimiter)
            if has_headers:
                next(reader)
            for row in reader:
                yield row


def dump_utf_json(entries, json_file):
    print(f"Dumping {len(entries)} entries into {json_file}...")
    with open(get_abs_path(json_file), 'w', encoding='utf-8') as handler:
        json.dump(entries, handler, ensure_ascii=False, sort_keys=True, indent=2)


def load_utf_json(json_file):
    with open(json_file, encoding='utf8') as data:
        return json.load(data)


def upsert_mongo_entry(coll, entry):
    try:
        coll.replace_one({'_id': entry['_id']}, entry)
    except KeyError:
        coll.insert_one(entry)
