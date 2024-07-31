from tkinter import *
from tkinter.colorchooser import *
from tkinter.filedialog import *

root = Tk()
root.title("Title")
root.geometry("500x500")

def SelectColor():
    color = askcolor()
    myLabel = Label(text="Hello Python",bg=color[1]).pack()

def SelectFile():
    fileOpen = askopenfile()
    FileContent = open(fileOpen,encoding="utf8")
    myLabel = Label(text=FileContent.read()).pack()

Btn1 = Button(text="เลือกสี",command=SelectColor).pack()
Btn2 = Button(text="เลือกไฟล์",command=SelectFile).pack()

root.mainloop()