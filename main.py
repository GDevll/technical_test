import sys


def UI_loop():

    for line in sys.stdin:
        line = line.rstrip()
        words = [word for word in line.split(' ') if word.strip()]

        if 'exit' == line:
            break

        if len(words) == 2 and words[0] == 'load':
            try:
                print("file loaded successfully")
            except Exception as exception:
                print("file can't be loaded try again: " + exception.args)
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