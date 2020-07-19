# technical_test

### Install
- The program required some some modules to pip install.
You can find them on requirements.txt

- Load th query from database.sql before any use of the program

- In order to launch the program, use this command from the root of the repo:

python3 main.py

### USER GUIDE

- load database [user] [password]: connect database.sql to the program.
user and password are the parameters to the connection to MariaDB (MySQL)

- load : load the default csvfile. This command take a time to be executed

- exit: close the connection to the database and stop the program

- top 10: return the 10 most expansive 3G connection outside 8h-18h per subscriber

- count sms: return the number of messages registered in the database

- sum call: sum the call duration after the 15 th  february 2012 included.