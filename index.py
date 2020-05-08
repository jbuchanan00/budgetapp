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

#Global Variables
userFirstName = ""
userLastName = ""
id = 0
inSourceFreq = IntVar()



user_info = ["no one"]

def login_submit():
    global userFirstName
    global userLastName
    global id
    cursor = conn.cursor()
    id = loginEntry.get()
    query = f'''select * from user_info where id = {id}'''
    cursor.execute(query)
    user_info = cursor.fetchall()
    print(user_info[0])
    cursor.close()
    #kills login screen without killing the main program
    loginScreen.withdraw()
    userFirstName = user_info[0][1].strip()
    userLastName = user_info[0][2].strip()
    userFirstNameLabel = Label(tk, text=userFirstName)
    userLastNameLabel = Label(tk, text=userLastName)
    userFirstNameLabel.grid(row=0, column=0)
    userLastNameLabel.grid(row=0, column=1)

def submitInClick():
    print(id, incomeSource.get(), inSourceFreq.get())






#Labels
userFirstNameLabel = Label(tk, text=userFirstName)
userLastNameLabel = Label(tk, text=userLastName)
loginLabel = Label(loginScreen, text="Login")
incomeSourceLabel = Label(tk, text="Income Source")
incomeSourceFreqLabel = Label(tk, text="Frequency of Income")


#Buttons
loginButton = Button(loginScreen, text="Login", command=lambda:login_submit())
submitIn = Button(tk, text="Submit", command=submitInClick)


#Inputs
loginEntry = Entry(loginScreen, width=60)
incomeSource = Entry(tk, width=30)

#RadioButton
incomeSourceOneTime = Radiobutton(tk, text="One Time", variable=inSourceFreq, value=1)
incomeSourceBiWeek = Radiobutton(tk, text="Bi-Weekly", variable=inSourceFreq, value=2)
incomeSourceMonth = Radiobutton(tk, text="Monthly", variable=inSourceFreq, value=3)
incomeSourceSemiAnn = Radiobutton(tk, text="Semi-Annually", variable=inSourceFreq, value=4)
incomeSourceYear = Radiobutton(tk, text="Yearly", variable=inSourceFreq, value=5)


#Layout
#Labels
loginLabel.grid(row=0, column=0)
userFirstNameLabel.grid(row=0, column=0)
userLastNameLabel.grid(row=0, column=1)
incomeSourceLabel.grid(row=1, column=0)

#Buttons
loginButton.grid(row=2, column=0)
submitIn.grid(row=4, column=1)

#Inputs
loginEntry.grid(row=1, column=0)
incomeSource.grid(row=2, column=0)

#RadioButtons
incomeSourceOneTime.grid(row=3, column=1)
incomeSourceBiWeek.grid(row=3, column=2)
incomeSourceMonth.grid(row=3, column=3)
incomeSourceSemiAnn.grid(row=3, column=4)
incomeSourceYear.grid(row=3, column=5)

loginScreen.mainloop()
tk.mainloop()
conn.close()


