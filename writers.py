from email import encoders as email_encoders
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
import smtplib

from pymongo import MongoClient

from global_vars import COLLOCATIONS, DB_NAME, FILE_PATH, LOCALHOST, PORT
from userinfo import EMAIL, EPSWRD


def to_email(file_path=FILE_PATH):
    smtp_server = "smtp.yandex.ru"
    smtp_port = 465

    msg = MIMEMultipart()
    msg["From"] = EMAIL
    msg["To"] = EPSWRD
    msg["Subject"] = 'fr_collocations'

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
    return f"10 {tag_count} tags, {mot_count} collocations ont été écrites dans le fichier {file_path}."


def del_by_tag(tag):
    print(f"Del {tag} from {DB_NAME}.{COLLOCATIONS}...")
    target = MongoClient(LOCALHOST, PORT)[DB_NAME][COLLOCATIONS]
    print(f"Initially, {target.estimated_document_count()} entries")
    target.delete_many({'tag': tag})
    print(f"Finally, {target.estimated_document_count()} entries")


if __name__ == '__main__':
    to_txt()
    # to_email()
