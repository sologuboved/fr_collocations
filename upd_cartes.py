import subprocess

from helpers import dump_utf_json, read_csv


def csv_to_json():
    dump_utf_json(list(read_csv('cartes.csv', as_dict=True)), 'cartes.json')
    subprocess.run(
        "sudo cp cartes.json /var/www/html/cartes/fran.json",
        shell=True,
    )


if __name__ == '__main__':
    csv_to_json()
