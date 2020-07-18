import csv
import mysql.connector
from datetime import datetime

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


def load_sub(row, db, cursor):

    subs = row["N° abonné\t"]

    sql_find_sub = "SELECT * FROM `phonedata`.`subscriber` WHERE `subscriber`=" + subs

    cursor.execute(sql_find_sub)
    records = cursor.fetchall()

    if (cursor.rowcount == 0):
        insert_sub(row, db, cursor)


def check_hour(hour):
    try:
        res = datetime.strptime(hour, '%H:%M:%S').strftime('%H:%M:%S')
    except:
        res = None

    return res

def verif_data(row):
    try:
        date = datetime.strptime(row["Date "], '%d/%m/%Y').strftime('%Y-%m-%d')
    except:
        date = None

    return (date, check_hour(row["Heure"]))



def format_duration(val):
    duration = val[3]
    billed_d = val[4]

    return (val[0], val[1],val[2], check_hour(duration), check_hour(billed_d))

def load_data_db(row, co, cursor):

    load_sub(row, co, cursor)

    subs = row["N° abonné\t"]
    typed = row["Type "]
    r_amount = row["Durée/volume réel"]
    i_amount = row["Durée/volume facturé"]
    (date, hour) = verif_data(row)

    sql = "INSERT INTO `phonedata`."
    val = (subs, date, hour, r_amount, i_amount)

    if typed.find("connexion") != -1:
        sql += "`Iconnection` (`subscriber`, `date`, `time`, `amount`, `billed_amount`) VALUES (%s, %s, %s, %s, %s)"
    elif typed.find("appel") != -1:
        val = format_duration(val)
        print(val)
        sql += "`call` (`subscriber`, `date`, `time`, `duration`, `billed_duration`) VALUES (%s, %s, %s, %s, %s)"
    elif typed.find("sms") != -1:
        #print("message")
        return 1
    elif typed.find("suivi conso") != -1:
        #print("suivi conso")
        return 1
    elif typed.find("messagerie vocale"):
        #print("messagerie vocale")
        return 1
    else:
        return 1

    cursor.execute(sql, val)
    co.commit()

    if cursor.rowcount == 0:
        return 1

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
