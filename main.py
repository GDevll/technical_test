import sys

import repository

def loading_cmd(words, db_cursor):
    if db_cursor is not None:
        print("A cvs file is already loaded")
        return db_cursor

    try:
        if len(words) == 2:
            db_cursor = repository.load_csvfile(words[1])
        else:
            db_cursor = repository.load_csvfile()

        print("file successfully loaded")

    except Exception as exception:
        print("file can't be loaded, try again: " + exception.args[0])

    return db_cursor

def UI_loop():

    db_cursor = None

    for line in sys.stdin:

        line = line.rstrip()
        words = [word for word in line.split(' ') if word.strip()]

        if not words:
            print('-', end='', flush=True)
            continue

        if 'exit' == line:
            break

        if words[0] == 'load' and len(words) <= 2:
            db_cursor = loading_cmd(words, db_cursor)
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