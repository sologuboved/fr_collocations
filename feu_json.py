import upd_json
import write


def main():
    upd_json.from_csv()
    write.backup(extention='json')
    print(write.json_to_txt())
    write.to_email()


if __name__ == '__main__':
    main()
