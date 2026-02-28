import datetime
from email import encoders as email_encoders
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
import os
import pathlib
import re
import smtplib

from pymongo import MongoClient

from global_vars import COLLOCATIONS, DB_NAME, FILE_PATH, LOCALHOST, PORT
from helpers import CsvWriter, read_csv
from userinfo import EMAIL, EPSWRD


def to_email(file_path=FILE_PATH):
    smtp_server = "smtp.yandex.ru"
    smtp_port = 465

    msg = MIMEMultipart()
    msg['From'] = EMAIL
    msg['To'] = EPSWRD
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


def to_txt(file_path=FILE_PATH):
    tag_count = mot_count = 0
    text = str()
    target = MongoClient(LOCALHOST, PORT)[DB_NAME][COLLOCATIONS]
    for tag in sorted(target.distinct('tag')):
        tag_count += 1
        text += tag.upper() + '\n'
        for entry in target.find({'tag': tag}).sort('mot', 1):
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


def to_csv():
    pathlib.Path('backups').mkdir(parents=True, exist_ok=True)
    backup_filename = os.path.join('backups', f'collocations{datetime.datetime.now():%Y%m%d%H%M%S%f}.csv')
    filename = 'collocations.csv'
    print(f"{DB_NAME}.{COLLOCATIONS} -> {backup_filename} & {filename}")
    rows = list(MongoClient(LOCALHOST, PORT)[DB_NAME][COLLOCATIONS].find(projection={'_id': 0}).sort('mot', 1))
    for target_filename in (backup_filename, filename):
        with CsvWriter(target_filename, ('mot', 'trad', 'tag')) as handler:
            handler.bulk(rows)
    print("...done. Deleting redundant files...")
    pattern = re.compile(r'collocations\d+')
    backups = sorted(filter(pattern.match, os.listdir('backups')))
    outdated = len(backups) - 10
    if outdated > 0:
        print(f"Removing {outdated} files...")
        for index in range(outdated):
            os.remove(os.path.join('backups', backups[index]))
        print("...done deleting redundant files")
    else:
        print("...nothing to remove")


def del_by_tag(tag):
    print(f"Del {tag} from {DB_NAME}.{COLLOCATIONS}...")
    target = MongoClient(LOCALHOST, PORT)[DB_NAME][COLLOCATIONS]
    print(f"Initially, {target.estimated_document_count()} entries")
    target.delete_many({'tag': tag})
    print(f"Finally, {target.estimated_document_count()} entries")


def restore(filepath=None, target_collname=COLLOCATIONS):
    if not filepath:
        pattern = re.compile(r'collocations\d+')
        filepath = os.path.join('backups', sorted(filter(pattern.match, os.listdir('backups')))[-1])
    print(f"Restoring {DB_NAME}.{target_collname} from {filepath}")
    target = MongoClient(LOCALHOST, PORT)[DB_NAME][target_collname]
    target.drop()
    target.insert_many(list(read_csv(filepath, as_dict=True)))
    print(f"Got {target.estimated_document_count()} entries")


if __name__ == '__main__':
    to_csv()
    to_txt()
    # to_email()
    # restore(target_collname=COLLOCATIONS + '_test')
