import os
import psycopg2
import sys
from private import dbcredentials





conn = psycopg2.connect(dbcredentials)

conn.set_session(autocommit=True)

cursor = conn.cursor()
input_id = 1

query = f'''select * from user_info where id = {input_id}'''

cursor.execute(query)

user_info = cursor.fetchall()
user_first_name = user_info[0][1].strip()
user_last_name = user_info[0][2].strip()
welcome = "Welcome, " + user_first_name + " " + user_last_name

cursor.close()

conn.close()