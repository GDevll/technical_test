import sys

import repository
import req_db



def loading_cmd(words, db_cursor):
    # if db_cursor is not None:
    #     print("A csv file is already loaded")
    #     return db_cursor
    try:
        if len(words) == 2 and words[1] == "database":
            db_co = repository.connect_database()
            print("database successfully connected")
            return db_co
    except Exception as exception:
        print("database can't be connected, try again: " + exception.args[0])

    try:
        if len(words) == 1:
            db_co = repository.load_csvfile()
        else:
            db_co = repository.load_csvfile(words[1])
        print("file successfully loaded")
    except Exception as exception:
        print("file can't be loaded, try again: " + exception.args[0])

    return db_co

def UI_loop():

    db_co = None

    for line in sys.stdin:

        line = line.rstrip()
        words = [word for word in line.split(' ') if word.strip()]

        if not words:
            print('-', end='', flush=True)
            continue

        if 'exit' == line:
            break
        elif words[0] == 'load' and len(words) <= 2:
            db_co = loading_cmd(words, db_co)
        elif words == ['count','sms']:
            req_db.count_sms(db_co)
        else:
            print("command not found: " + line)

        print('-', end='', flush=True)




def main():

    print("\ncall file analyser started")
    print("\nPlease initialized the process by entering:'load filename.csv'\n")
    print('-', end='', flush=True)

    UI_loop()

    print("call file analyser stopped")


if __name__ == '__main__':
    main()