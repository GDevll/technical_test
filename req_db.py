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

def sum_call(db):
    if db is None:
        print("Error, can't be applied\nNo database loaded...")
        return

    cursor = db.cursor()

    sql = " SELECT SEC_TO_TIME(SUM(TIME_TO_SEC(`duration`))) FROM `phonedata`.`call` WHERE DATEDIFF(`date`, '2012-02-15') >= 0"
    cursor.execute(sql)
    record = cursor.fetchall()

    for row in record:
        nb_sms = row[0]

        if (nb_sms == 0):
            print("There are no call.")
        else:
            print("There is " + str(nb_sms) + " of call duration.")