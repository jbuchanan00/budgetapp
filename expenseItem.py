import psycopg2
from tkinter import messagebox


def eIButtonClick(src, expAmount, expDate, expItemPop, conn):
    eIAmount = expAmount.get()
    eIDate = expDate.get()
    expItemPop.withdraw()
    cursor = conn.cursor()
    query = "select expense_id from Expense where expense_source = %s"
    cursor.execute(query, [src])
    expId = cursor.fetchall()[0][0]
    print(eIAmount, eIDate, expId)
    query = "insert into Expense_Line (expense_id, amount, date_gone) values (%s, %s, %s)"
    try:
        cursor.execute(query, [expId, eIAmount, eIDate])
        messagebox.showinfo("Success", "Success")
    except psycopg2.Error as e:
        messagebox.showinfo("Error", e)
    cursor.close()