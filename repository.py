import csv
import mysql.connector

# file: tickets_appels_201202.csv


def csv_loading(name):
    try:
        file = open(name, encoding='ISO-8859-1', newline='')
    except OSError as error:
        raise Exception("file not found")

    print("loading csv file: " + name)

    fname = ["Compte facturé", "N° Facture", "N° abonné\t", "Date ", "Heure", "Durée/volume réel", "Durée/volume facturé", "Type "]
    reader = csv.DictReader(file, delimiter=";", fieldnames=fname)

    return reader



def connect_database():
    co = mysql.connector.connect(user='gillian', password='password', database='phonedata')


def load_csvfile(name="tickets_appels_201202.csv"):

    csv_reader = csv_loading(name)
    co_db = connect_database()

    i = 0
    is_query = False
    for row in reader:
        if not is_query:
            if list(row.values()) == fname:
                is_query = True
            i+= 1
            continue

        print(row)
        break



        # #try:
        #     print(row['N° Facture'])
        # except:
        #     continue