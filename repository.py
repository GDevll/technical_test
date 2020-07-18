import csv
import mysql.connector
from datetime import datetime

# file: tickets_appels_201202.csv

#load the csv file
def csv_loading(name, fname):
    try:
        file = open(name, encoding='ISO-8859-1', newline='')
    except OSError:
        raise Exception("file not found")

    print("loading csv file: " + name)

    reader = csv.DictReader(file, delimiter=";", fieldnames=fname)

    return reader


#Connect the db to the program
def connect_database():
    co = mysql.connector.connect(user='gillian', password='password', database='phonedata')
    return co

#Insert a new subscriber in the Db
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

#Check if a new subscriber should be insert in the db
def load_sub(row, db, cursor):

    subs = row["N° abonné\t"]

    try:
        int(subs)
    except:
        return False

    sql_find_sub = "SELECT * FROM `phonedata`.`subscriber` WHERE `subscriber`=" + subs

    cursor.execute(sql_find_sub)
    cursor.fetchall()

    if cursor.rowcount == 0:
        if insert_sub(row, db, cursor) == False:
            return False

    return True

#check hour validity
def check_hour(hour):
    try:
        res = datetime.strptime(hour, '%H:%M:%S').strftime('%H:%M:%S')
    except:
        res = None

    return res

#Check date and Hour validity
def verif_data(row):
    try:
        date = datetime.strptime(row["Date "], '%d/%m/%Y').strftime('%Y-%m-%d')
        int(row["N° abonné\t"])
    except:
        return None

    hour = check_hour(row["Heure"])

    return (date, hour)


# Check duration as time
def format_duration(val):
    duration = check_hour(val[3])
    billed_d = check_hour(val[4])

    return (val[0], val[1],val[2], duration, billed_d)


def verify_float(val):
    try:
        float(val[3])
        float(val[4])
    except:
        return False

    return True

# Parse A row in several type of data and insert it in the Db
def load_data_db(row, co, cursor):

    if not load_sub(row, co, cursor):
        return 1

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
        sql += "`call` (`subscriber`, `date`, `time`, `duration`, `billed_duration`) VALUES (%s, %s, %s, %s, %s)"
    elif typed.find("sms") != -1:
        val = (subs, date, hour)
        sql += "`msg` (`subscriber`, `date`, `time`) VALUES (%s, %s, %s)"
    else:
        print("unsupported type: " + typed)
        return 1

    cursor.execute(sql, val)
    co.commit()

    if cursor.rowcount == 0:
        return 1

    return 0



# Read through each line of the CSV
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

        try:
            unexploitable_d += load_data_db(row, co_db, cursor)
        except:
            unexploitable_d += 1
            continue


    if not is_query:
        raise Exception("the file's structure is not correct")

    if unexploitable_d == 0:
        print("each datum has been processed")
    else:
        print(str(unexploitable_d) + " data haven't been processed")

    return co_db
