import mysql.connector

def count_sms(db):
    if db is None:
        print("Error, can't be applied\nNo database loaded...")
        return

    cursor = db.cursor()

    sql = "SELECT COUNT(`id`) FROM `phonedata`.`msg`"
    cursor.execute(sql)
    record = cursor.fetchall()

    for row in record:
        nb_sms = row[0]

        if (nb_sms == 0):
            print("There is no message.")
        elif nb_sms == 1:
            print("There is one message.")
        else:
            print("There are " + str(nb_sms) + " messages.")
