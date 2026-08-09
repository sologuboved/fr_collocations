import datetime
from email import encoders as email_encoders
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from operator import itemgetter
import os
import pathlib
import re
import shutil
import smtplib

from pymongo import MongoClient

from config import COLLOCATIONS, DB_NAME, FILE_PATH, LOCALHOST, PORT
from helpers import CsvWriter, load_utf_json, read_csv
from userinfo import EMAIL, EPSWRD


def del_by_tag_in_db(tag):
    print(f"Del {tag} from {DB_NAME}.{COLLOCATIONS}...")
    target = MongoClient(LOCALHOST, PORT)[DB_NAME][COLLOCATIONS]
    print(f"Initially, {target.estimated_document_count()} entries")
    target.delete_many({'tag': tag})
    print(f"Finally, {target.estimated_document_count()} entries")


def restore_db(filepath=None, target_collname=COLLOCATIONS):
    if not filepath:
        pattern = re.compile(r'collocations\d+')
        filepath = os.path.join('backups', sorted(filter(pattern.match, os.listdir('backups')))[-1])
    print(f"Restoring {DB_NAME}.{target_collname} from {filepath}")
    target = MongoClient(LOCALHOST, PORT)[DB_NAME][target_collname]
    target.drop()
    for entry in read_csv(filepath, as_dict=True):
        entry['trad'] = entry['trad'] or None
        target.insert_one(entry)
    print(f"Got {target.estimated_document_count()} entries")


def to_email(file_path=FILE_PATH):
    smtp_server = "smtp.yandex.ru"
    smtp_port = 465

    msg = MIMEMultipart()
    msg['From'] = EMAIL
    msg['To'] = EMAIL
    msg['Subject'] = 'fr_collocations'

    body = "Le document est ci-joint."
    msg.attach(MIMEText(body, 'plain'))

    with open(file_path, 'rb') as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
    email_encoders.encode_base64(part)
    part.add_header('Content-Disposition', f"attachment; filename= {file_path}")
    msg.attach(part)

    server = smtplib.SMTP_SSL(smtp_server, smtp_port)
    server.login(EMAIL, EPSWRD)
    server.sendmail(EMAIL, EMAIL, msg.as_string())
    server.quit()

    return f"Le fichier {file_path} a été envoyé à {EMAIL}."


def to_txt(entries, file_path):
    tag_count = mot_count = 0
    text = str()
    for tag in sorted(entries.keys()):
        tag_count += 1
        text += tag.upper() + '\n'
        for entry in sorted(entries[tag], key=itemgetter('mot')):
            try:
                text += " ~ ".join((entry['mot'], entry['trad'])) + '\n'
            except TypeError:
                text += entry['mot'] + '\n'
            mot_count += 1
        text += '\n'
    text = text[:-1]
    with open(file_path, 'w') as handler:
        handler.write(text)
    return f"{tag_count} tags, {mot_count} collocations ont été écrites dans le fichier {file_path}."


def db_to_txt(file_path=FILE_PATH):
    target = MongoClient(LOCALHOST, PORT)[DB_NAME][COLLOCATIONS]
    return to_txt(
        entries={tag: target.find({'tag': tag}) for tag in sorted(target.distinct('tag'))},
        file_path=file_path,
    )


def json_to_txt(file_path=FILE_PATH):
    return to_txt(
        entries=load_utf_json('collocations.json'),
        file_path=file_path,
    )


def backup(extention):
    dirname = extention + '_backups'
    pathlib.Path(dirname).mkdir(parents=True, exist_ok=True)
    backup_fname = os.path.join(
        dirname,
        f'collocations{datetime.datetime.now():%Y%m%d%H%M%S%f}.{extention}',
    )
    {'csv': backup_to_csv, 'json': backup_to_json}[extention](backup_fname=backup_fname)
    print("Suppression des fichiers redondants...")
    pattern = re.compile(r'collocations\d+')
    backups = sorted(filter(pattern.match, os.listdir(dirname)))
    outdated = len(backups) - 10
    if outdated > 0:
        print(f"{outdated} fichier(s) trouvé(s)...")
        for index in range(outdated):
            os.remove(os.path.join(dirname, backups[index]))
        print("...suppression des fichiers redondants terminée")
    else:
        print("...rien à supprimer")


def backup_to_csv(backup_fname):
    filename = 'collocations.csv'
    print(f"{DB_NAME}.{COLLOCATIONS} -> {backup_fname} & {filename}")
    rows = list(MongoClient(LOCALHOST, PORT)[DB_NAME][COLLOCATIONS].find(projection={'_id': 0}).sort('mot', 1))
    for target_filename in (backup_fname, filename):
        with CsvWriter(target_filename, ('mot', 'trad', 'tag')) as handler:
            handler.bulk(rows)
    print('...terminé')


def backup_to_json(backup_fname):
    print(f"Sauvegardons à {backup_fname}...")
    shutil.copy('collocations.json', backup_fname)
    print('...terminé')


if __name__ == '__main__':
    # restore(filepath='collocations.csv', target_collname=COLLOCATIONS)
    # to_csv()
    # to_txt()
    to_email()
