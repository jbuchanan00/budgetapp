import os
import psycopg2
import sys
from private import dbcredentials
from tkinter import *
from login import *


conn = psycopg2.connect(dbcredentials)
tk = Tk()
tk.geometry("1200x800")
#create login screen
loginScreen = Toplevel()
loginScreen.title("login")

conn.set_session(autocommit=True)



user_info = ["no one"]

def login_submit():
    cursor = conn.cursor()
    id = loginEntry.get()
    query = f'''select * from user_info where id = {id}'''
    cursor.execute(query)
    user_info = cursor.fetchall()
    print(user_info[0])
    cursor.close()
    #kills login screen without killing the main program
    loginScreen.withdraw()
    displayName = Label(tk, text=user_info[0])
    displayName.pack()

loginButton = Button(loginScreen, text="hope", command=lambda:login_submit())
loginEntry = Entry(loginScreen, width=60)


loginButton.grid(row=1, column=0)
loginEntry.grid(row=0, column=0)


loginScreen.mainloop()
tk.mainloop()
conn.close()


