from tkinter import *

root = Tk()
root.title("title")
root.geometry("500x500")

def ShowChoice():
    print(language.get(),language2.get(),language3.get())

language = IntVar()
Checkbutton(text="Python",variable=language).pack(anchor=W)
language2 = IntVar()
Checkbutton(text="Java",variable=language2).pack(anchor=W)
language3 = IntVar()
Checkbutton(text="Php",variable=language3).pack(anchor=W)
Button(text="Show",command=ShowChoice).pack()

root.mainloop()