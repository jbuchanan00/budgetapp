import os
import psycopg2
import sys
from private import *





conn = psycopg2.connect(db-credentials)

conn.set_session(autocommit=True)

cursor = conn.cursor()

query = '''select * from user_info'''

cursor.execute(query)

print(cursor.fetchall())

cursor.close()

conn.close()