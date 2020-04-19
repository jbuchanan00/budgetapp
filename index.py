import os
import psycopg2
import sys
from private import dbcredentials





conn = psycopg2.connect(dbcredentials)

conn.set_session(autocommit=True)

cursor = conn.cursor()

query = '''select * from user_info'''

cursor.execute(query)

print(cursor.fetchall())

cursor.close()

conn.close()