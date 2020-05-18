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
    cursor = conn.cursor()
    inSource = incomeSource.get()
    sourceFreq = inSourceFreq.get()
    query = 'insert into income (source, isfrequent, user_id) values (%s, %s, %s)'
    print(query)
    cursor.execute(query, (inSource, sourceFreq, id))
    cursor.close()


def getInfoClick():
    global id
    cursor = conn.cursor()
    query = f'select * from income where user_id = {id}'
    cursor.execute(query)
    info = cursor.fetchall()
    j = 6
    for i in info:
        
        if i[2] == 2:
            frequency = "Bi-Weekly"
        elif i[2] == 3:
            frequency = "Monthly"
        infoLabel = Label(tk, text=i[1].strip())
        frequencyLabel = Label(tk, text=frequency)
        infoLabel.grid(row=j, column=0)
        frequencyLabel.grid(row=j, column=1)
        j = j + 1
        





#Labels
userFirstNameLabel = Label(tk, text=userFirstName)
userLastNameLabel = Label(tk, text=userLastName)
loginLabel = Label(loginScreen, text="Login")
incomeSourceLabel = Label(tk, text="Income Source")
incomeSourceFreqLabel = Label(tk, text="Frequency of Income")


#Buttons
loginButton = Button(loginScreen, text="Login", command=lambda:login_submit())
submitIn = Button(tk, text="Submit", command=submitInClick)
incomeInfo = Button(tk, text="Income info", command=getInfoClick)


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
incomeSourceLabel.grid(row=1, column=1, columnspan=2)

#Buttons
loginButton.grid(row=2, column=0)
submitIn.grid(row=4, column=2)
incomeInfo.grid(row=5, column=0)

#Inputs
loginEntry.grid(row=1, column=0)
incomeSource.grid(row=2, column=1, columnspan=2)

#RadioButtons
incomeSourceOneTime.grid(row=3, column=0)
incomeSourceBiWeek.grid(row=3, column=1)
incomeSourceMonth.grid(row=3, column=2)
incomeSourceSemiAnn.grid(row=3, column=3)
incomeSourceYear.grid(row=3, column=4)

loginScreen.mainloop()
tk.mainloop()
conn.close()


