import sqlite3

db = "devdb.db"
connection = sqlite3.connect(db)
cursor = connection.cursor()
cursor.execute("SELECT * FROM fingerprints")
rows = cursor.fetchall()
connection.close()
for row in rows:
    print(row)