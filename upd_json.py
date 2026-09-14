from operator import itemgetter

from helpers import dump_utf_json, load_utf_json, read_csv


def add_tag(tag, fname='collocations.json'):
    print(f"Adding {tag}...")
    collocations = load_utf_json(fname)
    assert tag not in collocations, f"{tag} est déjà présent ; annulation !"
    collocations[tag] = list()
    dump_utf_json(collocations, fname)
    print('...done')


def from_csv(src_fname='mots_temp.csv', target_fname='collocations.json', drop=False):
    print(f"{src_fname} -> {target_fname}")
    if drop:
        collocations = dict()
    else:
        collocations = load_utf_json(target_fname)
    mots = [collocation['mot'] for val in collocations.values() for collocation in val]
    print(f"Initially, {len(mots)} entries")
    for row in read_csv(src_fname, as_dict=True):
        print(row)
        row = {key: val.strip() or None for key, val in row.items()}
        mot = row['mot']
        tag = row['tag']
        if mot in mots:
            print(f"'{mot}' est déjà présent ; on l'omet")
            continue
        try:
            collocations[tag].append(row)
        except KeyError:
            print(f"'{tag}' n'existe pas ; on l'omet (row {mot},{row['trad']},{tag})")
            continue
    print(f"Finally, {sum(len(val) for val in collocations.values())} entries")
    for tag in list(collocations.keys()):
        collocations[tag] = sorted(collocations[tag], key=itemgetter('mot'))
    dump_utf_json(collocations, target_fname)


if __name__ == '__main__':
    # add_tag('')
    from_csv(
        # target_fname='collocations_test.json',
    )
