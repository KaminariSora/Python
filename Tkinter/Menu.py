from tkinter import *
import tkinter.messagebox

root = Tk()
root.title("Menu")
root.geometry("500x500")



myMenu = Menu()
root.config(menu=myMenu)

def NewWindow():
    print("create new window")
    window_2 = Tk()
    window_2.geometry("200x200")
    window_2.title("second window")
    window_2.mainloop()

def About():
    print("About page")
    tkinter.messagebox.showinfo("About","Hello KaminariSora")

def ExitProgram():
    tkinter.messagebox.askquestion("R U sure?","Confirm?")
    root.destroy()

MenuItem = Menu()
MenuItem.add_command(label="New Text File")
MenuItem.add_command(label="New File")
MenuItem.add_command(label="New Window",command=NewWindow)
MenuItem.add_command(label="Exit",command=ExitProgram)

myMenu.add_cascade(label="File",menu=MenuItem)
myMenu.add_cascade(label="Option")
myMenu.add_cascade(label="About",command=About)
myMenu.add_cascade(label="Help")


root.mainloop()