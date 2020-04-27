from tkinter import *
from index import welcome

boolean = True

root = Tk()

def whatToShow():
    if(boolean):
        return "Hello friend"
    else:
        return "Hello enemy"
def clickedButton():
    boolean = False
    myLabel = Label(root, text=whatToShow())
    print(boolean)
    myLabel.pack()

button = Button(root, text="Click Here", command=clickedButton)
    

button.pack()


root.mainloop()