import mysql.connector

# Request the number of sms sent
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


# Request the sum of call's duration from the 15th february 2012
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



# Request the Top 10 billed_amount of data per subscriber
def best_customer(db):
    if db is None:
        print("Error, can't be applied\nNo database loaded...")
        return

    cursor = db.cursor()

    sql = '''SELECT `subscriber`, `billed_amount`, `time`
    FROM
        (SELECT `id`, `subscriber`, `billed_amount`, `time`,
                    @subscriber_rank := IF(@current_subscriber = `subscriber`, @subscriber_rank + 1, 1) AS subscriber_rank,
                    @current_subscriber := `subscriber`
        FROM (
            SELECT * FROM `phonedata`.`Iconnection`
            WHERE TIMEDIFF(`time`, '08:00:00') < 0 OR TIMEDIFF(`time`, '18:00:00') > 0
        ) AS tab
        ORDER BY `subscriber`, `billed_amount` DESC
        ) ranked
    WHERE subscriber_rank <= 10;'''
    cursor.execute(sql)
    record = cursor.fetchall()
    cursor.execute(sql)
    record = cursor.fetchall()

    customer  = None
    i = 10
    for row in record:
        if customer != row[0]:
            i = 10
            customer = row[0]
            print("-------------------")
            print("TOP 10 subscriber : " + str(customer))

        print(str(i) + "---" + "amount: " + str(row[1]) + "    time: " + str(row[2]))
        i -= 1