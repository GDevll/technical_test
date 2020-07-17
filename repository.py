import csv

# file: tickets_appels_201202.csv

def load_csvfile(name):

    try:
        file = open(name, encoding='ISO-8859-1', newline='')
    except OSError as error:
        raise Exception("file not found")

    print("loading csv file: " + name)

    fname = ["Compte facturé", "N° Facture", "N° abonné", "Date", "Heure", "Durée/volume réel", "Durée/volume facturé", "Type"]
    reader = csv.DictReader(file, delimiter=";", fieldnames=fname)

    for row in reader:

        try:
            print(row['N° Facture'])
        except:
            continue

        i += 1


