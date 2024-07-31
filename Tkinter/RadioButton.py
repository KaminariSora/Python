from tkinter import *
import tkinter.messagebox

root = Tk()
root.title("title")
root.geometry("500x500")

def ShowChoice():
    choice = language.get()
    if choice == 1:
        tkinter.messagebox.showinfo("alert","You have selected C#")
    elif choice == 2:
        tkinter.messagebox.showinfo("alert","You have selected Java")
    elif choice == 3:
        tkinter.messagebox.showinfo("alert","You have selected Python")
    elif choice == 4:
        tkinter.messagebox.showinfo("alert","You have selected JavaScript")
    print(choice)

language = IntVar()
language.set(5)
Radiobutton(text="C#",variable=language,value=1,command=ShowChoice).grid(row=0,column=0)
Radiobutton(text="Java",variable=language,value=2,command=ShowChoice).grid(row=0,column=1)
Radiobutton(text="Python",variable=language,value=3,command=ShowChoice).grid(row=0,column=2)
Radiobutton(text="JavaScript",variable=language,value=4,command=ShowChoice).grid(row=0,column=3)
Radiobutton(text="Default(none)",variable=language,value=5).grid(row=0,column=4)

root.mainloop()