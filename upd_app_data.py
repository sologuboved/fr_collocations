import subprocess

from helpers import dump_utf_json, read_csv


def upd(front, back, f_json, src_csv, sort, push):
    if src_csv:
        data = [dict(zip((back, front), map(str.strip, row))) for row in read_csv(src_csv, as_dict=False)]
        if sort:
            data.sort(key=lambda x: (len(x[front]), x[back],))
        dump_utf_json(data, f_json)
    if push:
        for command in (
            f"git add {f_json}",
            'git commit -m "upd"',
            "git push origin main",
        ):
            print(command + '...')
            subprocess.run(command, shell=True)


def upd_coi(from_csv=False, sort=False, push=True):
    upd(front='préposition', back='verbe', f_json='coi.json', src_csv=[None, 'coi.csv'][from_csv], sort=sort, push=push)


def upd_cartes(from_csv=False, sort=False, push=True):
    upd(front='mot', back='trad', f_json='cartes.json', src_csv=[None, 'cartes.csv'][from_csv], sort=sort, push=push)


if __name__ == '__main__':
    upd_coi(
        from_csv=True,
        sort=True,
        # push=False,
    )
    # upd_cartes(
    #     from_csv=True,
    #     sort=True,
    #     push=False,
    # )
