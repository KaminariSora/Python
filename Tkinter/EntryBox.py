from tkinter import *
from tkinter import ttk

root = Tk()
root.title("title")
root.geometry("200x200+1000+100")

Label(text="Name").grid(row=0)
Label(text="LastName").grid(row=1)
Label(text="Phone").grid(row=2)
Label(text="Place").grid(row=3,column=0)

et1 = Entry()
et1.grid(row=0,column=1)
et1.insert(0,"Sora")

et2 = Entry()
et2.grid(row=1,column=1)
et2.insert(0,"Kaminari")

et3 = Entry()
et3.grid(row=2,column=1)
et3.insert(0,"xxx-xxx-xxxx")

choice = StringVar(value="choose your place")
combo = ttk.Combobox(textvariable=choice)
combo["values"] = ("TH","USA","JP","CN")
combo.grid(row=3,column=1)

def ClearText():
    et1.delete(0, END)
    et2.delete(0, END)
    et3.delete(0, END)

button = Button(text="Clear",command=ClearText).grid(row=4,column=1)

root.mainloop()