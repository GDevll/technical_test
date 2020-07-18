import csv
import mysql.connector

# file: tickets_appels_201202.csv


def csv_loading(name, fname):
    try:
        file = open(name, encoding='ISO-8859-1', newline='')
    except OSError as error:
        raise Exception("file not found")

    print("loading csv file: " + name)

    reader = csv.DictReader(file, delimiter=";", fieldnames=fname)

    return reader



def connect_database():
    co = mysql.connector.connect(user='gillian', password='password', database='phonedata')
    return co


def insert_sub(row, db, cursor):
    account = row["Compte facturé"]
    invoice = row["N° Facture"]
    subs = row["N° abonné\t"]

    sql_insert = "INSERT INTO `phonedata`.`subscriber` (`invoice_acc`, `invoice`, `subscriber`) VALUES (%s, %s, %s)"
    val = (account, invoice, subs)
    cursor.execute(sql_insert, val)

    db.commit()

    if cursor.rowcount == 0:
        raise Exception("Error subscriber insertion")
    else:
        print("Yes")



def load_sub(row, db, cursor):

    subs = row["N° abonné\t"]

    sql_find_sub = "SELECT * FROM `phonedata`.`subscriber` WHERE `subscriber`=" + subs

    cursor.execute(sql_find_sub)
    records = cursor.fetchall()

    if (cursor.rowcount == 0):
        insert_sub(row, db, cursor)



def load_data_db(row, co, cursor):

    load_sub(row, co, cursor)

    subs = row["N° abonné\t"]
    typed = row["Type "]
    date = row["Date "]
    hour = row["Heure"]
    r_amount = row["Durée/volume réel"]
    i_amount = row["Durée/volume facturé"]

    sql = "INSERT INTO phonedata."
    val = ("","")

    if typed.find("connexion") != -1:
        print("connexion")

    elif typed.find("appel") != -1:
        print("call")
    elif typed.find("sms") != -1:
        print("message")
    elif typed.find("suivi conso") != -1:
        print("suivi conso")
    elif typed.find("messagerie vocale"):
        print("messagerie vocale")
    else:
        return 1


    co.commit()


    return 0




def load_csvfile(name="tickets_appels_201202.csv"):

    fname = ["Compte facturé", "N° Facture", "N° abonné\t", "Date ", "Heure", "Durée/volume réel", "Durée/volume facturé", "Type "]
    csv_reader = csv_loading(name, fname)
    co_db = connect_database()
    cursor = co_db.cursor()

    unexploitable_d = 0

    i = 0
    is_query = False
    for row in csv_reader:

        if not is_query:
            if list(row.values()) == fname:
                is_query = True
            i+= 1
            continue

        unexploitable_d += load_data_db(row, co_db, cursor)


    if not is_query:
        raise Exception("the file's structure is not correct")

    if unexploitable_d == 0:
        print("each datum has been processed")
    else:
        print(str(unexploitable_d) + " data haven't been processed")
