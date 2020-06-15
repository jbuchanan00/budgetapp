import psycopg2
from tkinter import messagebox

def expenseEntryClick(expenseSrc, clicked, catIdFind, exSourceFreq, id, conn):
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