import subprocess

from helpers import dump_utf_json, read_csv


def main(sort=True):
    cartes = list(read_csv('cartes.csv', as_dict=True))
    if sort:
        cartes.sort(key=lambda x: (len(x['trad']), x['mot'],))
    dump_utf_json(cartes, 'cartes.json')
    for command in (
        "git add cartes.json",
        'git commit -m "upd"',
        "git push origin main",
    ):
        print(command + '...')
        subprocess.run(command, shell=True)


if __name__ == '__main__':
    main()
