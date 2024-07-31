from tkinter import *

root = Tk()
root.title("My GUI")

myLabel = Label(root,text="Hello World",fg='green',font=20,bg="brown").pack()

# ปุ่มกด
def ShowMessage():
    print("Hello World")
    Label(root,text="Hello World",fg='red',font=20,bg="brown").pack()

btn1 = Button(text="Open",bg="yellow",command=ShowMessage).pack()
btn2 = Button(text="Open",bg="green").pack()

# กล่องข้อความ
txt = StringVar()
myText = Entry(root,textvariable=txt).pack()

# กำหนดขนาดหน้าจอ
root.geometry("500x400+50+50")

# รันโปรแกรม
root.mainloop()