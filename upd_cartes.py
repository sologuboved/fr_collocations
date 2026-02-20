import subprocess

from helpers import dump_utf_json, read_csv


def main():
    dump_utf_json(list(read_csv('cartes.csv', as_dict=True)), 'cartes.json')
    for command in (
        "git add cartes.json",
        'git commit -m "upd"',
        "git push origin main",
    ):
        print(command + '...')
        subprocess.run(command, shell=True)


if __name__ == '__main__':
    main()
