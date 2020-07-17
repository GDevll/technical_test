import sys


def main():

    print("call file analyser started")
    print("Please initialized the process by entering:'charge filename.csv'")
    print('-', end='')

    for line in sys.stdin:
        if 'exit' == line.rstrip():
            break
        print("I watched this: " + line.rstrip())
        print('-', end='')


if __name__ == '__main__':
    main()