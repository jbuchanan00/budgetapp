import os
import psycopg2
import sys
from private import dbcredentials
from tkinter import *
from login import *
from datetime import date
from tkinter import messagebox


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
    global incomeSource
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
        if i[2] == 1:
            frequency = "One Time"
        elif i[2] == 2:
            frequency = "Bi-Weekly"
        elif i[2] == 3:
            frequency = "Monthly"
        elif i[2] == 4:
            frequency = "Semi-Annually"
        elif i[2] == 5:
            frequency = "Annually"
        else:
            frequency = "Not specified"
        source = i[1].strip()
        infoButton = Button(tk, text=i[1].strip())
        frequencyLabel = Label(tk, text=frequency)
        infoButton.bind("<Button-1>", infoButtonClick)
        infoButton.grid(row=incomeRow, column=0)
        frequencyLabel.grid(row=incomeRow, column=1)
        incomeRow = incomeRow + 1
        j += 1
    cursor.close()
    
def infoButtonClick(event):
    global incomeAmount
    global incomeDate
    global incomeItemPop
    button = (event.widget)
    incomeName = button.cget("text")
    incomeItemPop = Toplevel()
    incomeItemPop.title("Income Entry")
    #Widgets
    incomeAmount = Entry(incomeItemPop, width=30)
    incomeDate = Entry(incomeItemPop, width=30)
    incomeItemSubmit = Button(incomeItemPop, text="Submit", padx=5, pady=5, command=lambda: iIButtonClick(incomeName))
    #Inserts
    incomeDate.insert(0, date.today())
    #Placements
    incomeAmount.grid(row=0, column=0)
    incomeDate.grid(row=0, column=1)
    incomeItemSubmit.grid(row=1, column=1, sticky=E)

    incomeItemPop.mainloop()

def iIButtonClick(src):
    global incomeAmount
    global incomeDate
    global incomeItemPop
    iIAmount = incomeAmount.get()
    iIDate = incomeDate.get()
    incomeItemPop.withdraw()
    cursor = conn.cursor()
    query = "select income_id from Income where source = %s"
    cursor.execute(query, [src])
    incomeId = cursor.fetchall()[0][0]
    print(iIAmount, iIDate, src, incomeId)
    lineQuery = "insert into income_line (income_id, amount, date_made) values (%s, %s, %s)"
    try:
        cursor.execute(lineQuery, [incomeId, iIAmount, iIDate])
        messagebox.showinfo("Success", "Success")
    except psycopg2.Error as e:
        messagebox.showinfo("Error", e)
    cursor.close()
    
    #IncomeID, Amount, Date

def incomeScreenClick():
    global tk
    global incomeSource
    for widget in tk.winfo_children():
        widget.destroy()
    incomeScreenButton = Button(tk, text="Income", command=incomeScreenClick)
    expenseScreenButton = Button(tk, text="Expense", command=expenseScreenClick)
    incomeScreenButton.grid(row=0, column=3)
    expenseScreenButton.grid(row=0, column=4)
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

def expenseScreenClick():
    global tk
    global userFirstName
    global userLastName
    global categoryEntry
    global expenseSrc
    global clicked
    global catIdFind
    global exSourceFreq
    for widget in tk.winfo_children():
        widget.destroy()
    #Widget
    #Label
    userFirstNameLabel = Label(tk, text=userFirstName)
    userLastNameLabel = Label(tk, text=userLastName)
    expenseLabel = Label(tk, text="Expenses")
    expCatLabel = Label(tk, text="Category")
    #Button
    incomeScreenButton = Button(tk, text="Income", command=incomeScreenClick)
    expenseScreenButton = Button(tk, text="Expense", command=expenseScreenClick)
    expenseSrcButton = Button(tk, text="Submit", command=expenseEntryClick)
    categoryEntryButton = Button(tk, text="Submit", command=categoryEntryClick)
    expenseInfoButton = Button(tk, text="Expense info", command=expenseInfoClick)
    #Entry
    categoryEntry = Entry(tk, width=30)
    categoryEntry.insert(0, "Category")
    expenseSrc = Entry(tk, width=30)
    expenseSrc.insert(0, "Source")
    #Radio Button
    exSourceFreq = IntVar()
    expenseSourceOneTime = Radiobutton(tk, text="One Time", variable=exSourceFreq, value=1)
    expenseSourceWeekly = Radiobutton(tk, text="Weekly", variable = exSourceFreq, value=2)
    expenseSourceBiWeek = Radiobutton(tk, text="Bi-Weekly", variable=exSourceFreq, value=3)
    expenseSourceMonth = Radiobutton(tk, text="Monthly", variable=exSourceFreq, value=4)
    expenseSourceSemiAnn = Radiobutton(tk, text="Semi-Annually", variable=exSourceFreq, value=5)
    expenseSourceYear = Radiobutton(tk, text="Yearly", variable=exSourceFreq, value=6)
    #Drop Menu
    clicked = StringVar()
    cursor = conn.cursor()
    cursor.execute("select * from category")
    fullCatList = cursor.fetchall()
    categoryList = []
    catIdFind = []
    for i in fullCatList:
        categoryList.append(i[1].strip())
        catIdFind.append(i)
    catDrop = OptionMenu(tk, clicked, *categoryList)
    
    #Layout
    #Label
    userFirstNameLabel.grid(row=0, column=0)
    userLastNameLabel.grid(row=0, column=1)
    expenseLabel.grid(row=1, column=1)
    expCatLabel.grid(row=7, column=1)
    #Button
    incomeScreenButton.grid(row=0, column=3)
    expenseScreenButton.grid(row=0, column=4)
    expenseSrcButton.grid(row=3, column=1)
    categoryEntryButton.grid(row=6, column=1)
    expenseInfoButton.grid(row=7, column=0)
    #Entry
    categoryEntry.grid(row=5, column=0, columnspan=3)
    expenseSrc.grid(row=2, column=0, columnspan=3)
    #Radio Button
    expenseSourceOneTime.grid(row=4, column=0)
    expenseSourceWeekly.grid(row=4, column=1)
    expenseSourceBiWeek.grid(row=4, column=2)
    expenseSourceMonth.grid(row=4, column=3)
    expenseSourceSemiAnn.grid(row=4, column=4)
    expenseSourceYear.grid(row=4, column=5)
    #Drop Menu
    catDrop.grid(row=2, column=3)

def categoryEntryClick():
    global categoryEntry
    cursor = conn.cursor()
    catEnt = categoryEntry.get()
    query = "insert into category (cat_name) values (%s)"
    try:
        cursor.execute(query, [catEnt])
        messagebox.showinfo("Success", "Success")
    except psycopg2.Error as e:
        messagebox.showinfo("Error", e)

def expenseEntryClick():
    global expenseSrc
    global clicked
    global catIdFind
    global exSourceFreq
    global id
    expEnt = expenseSrc.get()
    catEnt = clicked.get()
    freq = exSourceFreq.get()
    cursor = conn.cursor()
    catId = 0
    for i in catIdFind:
        print(i[1], catEnt)
        if i[1].strip() == catEnt:
            catId = i[0]
    #UserId, Source, Freq, Category
    query = "insert into Expense (user_id, expense_source, frequency, category_id) values (%s, %s, %s, %s)"
    try:
        cursor.execute(query, [id, expEnt, freq, catId])
        messagebox.showinfo("Success", "Success")
    except psycopg2.Error as e:
        messagebox.showinfo("Error", e)

def expenseInfoClick():
    global id
    cursor = conn.cursor()
    query = f"select * from Expense left join Category on Category.category_id = Expense.category_id where user_id = {id}"
    cursor.execute(query)
    info = cursor.fetchall()
    expRow = 8
    for i in info:
        print(i)
        expInfoButton = Button(tk, text=i[2].strip(), command=expLineClick)
        expInfoButton.grid(row=expRow, column=0)
        expCatInfo = Label(tk, text=i[6].strip())
        expCatInfo.grid(row=expRow, column=1)
        expInfoButton.bind("<Button-1>", expLineClick)
        expRow += 1  

def expLineClick(event):
    global expAmount
    global expDate
    global expItemPop
    button = (event.widget)
    expenseName = button.cget("text")
    expItemPop = Toplevel()
    expItemPop.title("Income Entry")
    #Widgets
    expAmount = Entry(expItemPop, width=30)
    expDate = Entry(expItemPop, width=30)
    expItemSubmit = Button(expItemPop, text="Submit", padx=5, pady=5, command=lambda: eIButtonClick(expenseName))
    #Inserts
    expDate.insert(0, date.today())
    #Placements
    expAmount.grid(row=0, column=0)
    expDate.grid(row=0, column=1)
    expItemSubmit.grid(row=1, column=1, sticky=E)

    expItemPop.mainloop()

def eIButtonClick(src):
    global expAmount
    global expDate
    global expItemPop
    eIAmount = expAmount.get()
    eIDate = expDate.get()
    expItemPop.withdraw()
    print(eIAmount, eIDate)
    

    
#Login/MainPage
#Labels
loginLabel = Label(loginScreen, text="Login")

#Buttons
loginButton = Button(loginScreen, text="Login", command=lambda:login_submit())
incomeScreenButton = Button(tk, text="Income", command=incomeScreenClick)
expenseScreenButton = Button(tk, text="Expense", command=expenseScreenClick)


#Inputs
loginEntry = Entry(loginScreen, width=60)

#Layout
#Labels
loginLabel.grid(row=0, column=0)

#Buttons
loginButton.grid(row=2, column=0)
incomeScreenButton.grid(row=0, column=3)
expenseScreenButton.grid(row=0, column=4)

#Inputs
loginEntry.grid(row=1, column=0)

loginScreen.mainloop()
tk.mainloop()
conn.close()


