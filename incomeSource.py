import psycopg2
from tkinter import messagebox

def submitInClick(incomeSource, conn, inSourceFreq, id):
    cursor = conn.cursor()
    inSource = incomeSource.get()
    sourceFreq = inSourceFreq.get()
    query = "select source from income where user_id = %s"
    cursor.execute(query, [id])
    inSourceCheck = cursor.fetchall()
    for i in inSourceCheck:
        print(i[0].strip())
        if(i[0].strip().upper() == inSource.upper()):
            messagebox.showinfo("Error", "Income source has already been submitted")
            return
        else:
            continue
    query = 'insert into income (source, isfrequent, user_id) values (%s, %s, %s)'
    try:
        cursor.execute(query, (inSource, sourceFreq, id))
        messagebox.showinfo("Success", "Success")
    except psycopg2.Error as e:
        messagebox.showinfo("Error", e)
    cursor.close()