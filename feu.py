import sys

import upd_db
import write


def main():
    upd_db.from_csv()
    argv = sys.argv
    if len(argv) == 1:
        write.to_csv()
        write.to_txt()
    else:
        if argv[-1] == 'e':
            write.to_email()
        else:
            print("Utilisez 'e' pour envoyer un courriel.")


if __name__ == '__main__':
    main()
