import sys

import repository



def UI_loop():

    for line in sys.stdin:

        line = line.rstrip()
        words = [word for word in line.split(' ') if word.strip()]

        if not words:
            print('-', end='')
            continue

        if 'exit' == line:
            break

        if words[0] == 'load' and len(words) <= 2:

            try:
                if len(words) == 2:
                    repository.load_csvfile(words[1])
                else:
                    repository.load_csvfile()

                print("file successfully loaded")
            except Exception as exception:
                print("file can't be loaded, try again: " + exception.args[0])

        else:
            print("command not found: " + line)

        print('-', end='')




def main():

    print("\ncall file analyser started")
    print("\nPlease initialized the process by entering:'load filename.csv'\n")
    print('-', end='')

    UI_loop()

    print("call file analyser stopped")


if __name__ == '__main__':
    main()