import csv


def load_csvfile(name):

    try:
        file = open(name, newline='')
    except OSError as error:
        raise Exception("error")

    print("loading csv file: " + name)


