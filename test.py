import os
import cx_Oracle

conn = cx_Oracle.connect(os.getenv('dbcred', 'dbms/dbms1234@localhost:1521'))
cursor = conn.cursor()
conn.commit()

for user in cursor.execute("SELECT * FROM USERS"):
    print(user)
