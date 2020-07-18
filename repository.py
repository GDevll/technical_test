import csv
import mysql.connector
from datetime import datetime

# file: tickets_appels_201202.csv


def csv_loading(name, fname):
    try:
        file = open(name, encoding='ISO-8859-1', newline='')
    except OSError:
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

    try:
        int(account)
        int(invoice)
    except:
        return False

    sql_insert = "INSERT INTO `phonedata`.`subscriber` (`invoice_acc`, `invoice`, `subscriber`) VALUES (%s, %s, %s)"
    val = (account, invoice, subs)
    cursor.execute(sql_insert, val)

    db.commit()

    if cursor.rowcount == 0:
        raise Exception("Error subscriber insertion")

    return True


def load_sub(row, db, cursor):

    subs = row["N° abonné\t"]

    try:
        int(subs)
    except:
        return False

    sql_find_sub = "SELECT * FROM `phonedata`.`subscriber` WHERE `subscriber`=" + subs

    cursor.execute(sql_find_sub)
    cursor.fetchall()

    if (cursor.rowcount == 0):
        if insert_sub(row, db, cursor) == False:
            return False

    return True


def check_hour(hour):
    try:
        res = datetime.strptime(hour, '%H:%M:%S').strftime('%H:%M:%S')
    except:
        res = None

    return res

def verif_data(row):
    try:
        date = datetime.strptime(row["Date "], '%d/%m/%Y').strftime('%Y-%m-%d')
        int(row["N° abonné\t"])
    except:
        return None

    hour = check_hour(row["Heure"])

    if hour is None:
        return None

    return (date, hour)



def format_duration(val):
    duration = check_hour(val[3])
    billed_d = check_hour(val[4])

    if duration is None or billed_d is None:
        return None

    return (val[0], val[1],val[2], duration, billed_d)


def verify_float(val):
    try:
        float(val[3])
        float(val[4])
    except:
        return False

    return True


def load_data_db(row, co, cursor):

    if not load_sub(row, co, cursor):
        return 1

    subs = row["N° abonné\t"]
    typed = row["Type "]
    r_amount = row["Durée/volume réel"]
    i_amount = row["Durée/volume facturé"]
    if verif_data(row) is None:
        return 1
    (date, hour) = verif_data(row)

    sql = "INSERT INTO `phonedata`."
    val = (subs, date, hour, r_amount, i_amount)

    if typed.find("connexion") != -1:
        if not verify_float(val):
            return 1
        sql += "`Iconnection` (`subscriber`, `date`, `time`, `amount`, `billed_amount`) VALUES (%s, %s, %s, %s, %s)"
    elif typed.find("appel") != -1:
        val = format_duration(val)
        if val is None:
            return 1
        sql += "`call` (`subscriber`, `date`, `time`, `duration`, `billed_duration`) VALUES (%s, %s, %s, %s, %s)"
    elif typed.find("sms") != -1:
        val = (subs, date, hour)
        sql += "`msg` (`subscriber`, `date`, `time`) VALUES (%s, %s, %s)"
    elif typed.find("suivi conso") != -1:
        print("unsupported: suivi conso")
        return 1
    elif typed.find("messagerie vocale") != -1:
        print("unsupported: messagerie vocale")
        return 1
    else:
        print("unsupported type: " + typed)
        return 1

    cursor.execute(sql, val)
    co.commit()

    if cursor.rowcount == 0:
        return 1

    return 0




def load_csvfile(name="tickets_appels_201202.csv"):

    fname = ["Compte facturé", "N° Facture", "N° abonné\t", "Date ", "Heure", "Durée/volume réel", "Durée/volume facturé", "Type "]
    csv_reader = csv_loading(name, fname)

    try:
        co_db = connect_database()
    except:
        raise Exception("database not found")

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

    return co_db
