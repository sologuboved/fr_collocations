import sys

import upd_json
import write


def main():
    upd_json.from_csv()
    write.backup(extention='json')
    print(write.json_to_txt())
    argv = sys.argv
    if argv[-1] == 'e':
        write.to_email()


if __name__ == '__main__':
    main()
