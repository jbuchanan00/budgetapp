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
    global incomeRow
    global infoButton
    cursor = conn.cursor()
    query = f'select * from income where user_id = {id}'
    cursor.execute(query)
    info = cursor.fetchall()
    incomeRow = 6
    j=0
    for i in info:
        if i[2] == 2:
            frequency = "Bi-Weekly"
        elif i[2] == 3:
            frequency = "Monthly"
        source = i[1].strip()
        infoButton = Button(tk, text=i[1].strip(), command=lambda: incomeItem(i))
        frequencyLabel = Label(tk, text=frequency)
        infoButton.bind("<Button-1>", infoButtonClick)
        infoButton.grid(row=incomeRow, column=0)
        frequencyLabel.grid(row=incomeRow, column=1)
        incomeRow = incomeRow + 1
        j += 1
    
def infoButtonClick(event):
    button = (event.widget)
    print(button.cget("text"))

def incomeItem(src):
    global incomeRow
    incomeItem = Entry(tk, width=30)
    incomeItemDate = Entry(tk, width=30)
    incomeItem.grid(row=incomeRow, column=2, columnspan=2)
    incomeItemDate.grid(row=incomeRow, column=4, columnspan=2)



def incomeScreenClick():
    #Income screen Labels
    userFirstNameLabel = Label(tk, text=userFirstName)
    userLastNameLabel = Label(tk, text=userLastName)
    incomeSourceLabel = Label(tk, text="Income Source")
    #Income screen Buttons
    submitIn = Button(tk, text="Submit", command=submitInClick)
    incomeInfo = Button(tk, text="Income info", command=getInfoClick)
    #Income screen Entries 
    incomeSource = Entry(tk, width=30)
    #Income screen Radio Buttons 
    incomeSourceOneTime = Radiobutton(tk, text="One Time", variable=inSourceFreq, value=1)
    incomeSourceBiWeek = Radiobutton(tk, text="Bi-Weekly", variable=inSourceFreq, value=2)
    incomeSourceMonth = Radiobutton(tk, text="Monthly", variable=inSourceFreq, value=3)
    incomeSourceSemiAnn = Radiobutton(tk, text="Semi-Annually", variable=inSourceFreq, value=4)
    incomeSourceYear = Radiobutton(tk, text="Yearly", variable=inSourceFreq, value=5)
    #Income screen grid placement
    #Labels
    userFirstNameLabel.grid(row=0, column=0)
    userLastNameLabel.grid(row=0, column=1)
    incomeSourceLabel.grid(row=1, column=1, columnspan=2)
    #Buttons
    submitIn.grid(row=4, column=2)
    incomeInfo.grid(row=5, column=0)
    #Entries
    incomeSource.grid(row=2, column=1, columnspan=2)
    #Radio Buttons
    incomeSourceOneTime.grid(row=3, column=0)
    incomeSourceBiWeek.grid(row=3, column=1)
    incomeSourceMonth.grid(row=3, column=2)
    incomeSourceSemiAnn.grid(row=3, column=3)
    incomeSourceYear.grid(row=3, column=4) 

#Login/MainPage
#Labels
loginLabel = Label(loginScreen, text="Login")

#Buttons
loginButton = Button(loginScreen, text="Login", command=lambda:login_submit())
incomeScreenButton = Button(tk, text="Income", command=incomeScreenClick)


#Inputs
loginEntry = Entry(loginScreen, width=60)

#Layout
#Labels
loginLabel.grid(row=0, column=0)

#Buttons
loginButton.grid(row=2, column=0)
incomeScreenButton.grid(row=0, column=3)

#Inputs
loginEntry.grid(row=1, column=0)

loginScreen.mainloop()
tk.mainloop()
conn.close()


