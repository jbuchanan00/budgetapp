import os
import psycopg2
import sys
from private import dbcredentials
from tkinter import *
from login import *


conn = psycopg2.connect(dbcredentials)
tk = Tk()
loginScreen = Toplevel()
loginScreen.title("login")

conn.set_session(autocommit=True)



user_info = []

def login_submit(id):
    cursor = conn.cursor()
    query = f'''select * from user_info where id = {id}'''
    cursor.execute(query)
    print(cursor.fetchall())
    cursor.close()
    loginScreen.withdraw()

loginButton = Button(loginScreen, text="hope", command=lambda:login_submit(1))
loginEntry = Entry(loginScreen, width=60)

loginButton.grid(row=1, column=0)
loginEntry.grid(row=0, column=0)

loginScreen.mainloop()
tk.mainloop()
conn.close()


