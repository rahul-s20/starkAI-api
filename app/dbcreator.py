import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="123456789"
)

myCursor = mydb.cursor()

myCursor.execute("CREATE DATABASE stark_dev")
myCursor.execute("SHOW DATABASES")

for db in myCursor:
    print(db)