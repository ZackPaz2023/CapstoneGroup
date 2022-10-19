import mysql.connector as mysql

host = "localhost"
user = "root"
password = "password"

try:
    db = mysql.connect(host=host, user=user, password=password, database="test")
    print("Connected to Database Successfully")
except Exception as e:
    print("Connection to Database not successful")
    print(e)

cursor = db.cursor()