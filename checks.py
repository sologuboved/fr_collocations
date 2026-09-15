from helpers import load_utf_json


def find_discrepancies_between_keys_and_tags(fname='collocations.json'):
    count = 0
    collocations = load_utf_json(fname)
    for key in collocations:
        for collocation in collocations[key]:
            tag = collocation['tag']
            if tag != key:
                print(f"KEY: {key}; TAG: {tag}; {collocation['mot']}")
                count += 1
    print(count)


if __name__ == '__main__':
    find_discrepancies_between_keys_and_tags()
