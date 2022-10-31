#!/usr/bin/python
# -*- coding: utf-8 -*-
from tkinter import *
import subprocess as sp

root = Tk()
root.title('Home Page')
root.geometry('600x350')


def gotoissue():
    root.destroy()
    sp.call('issue.py', shell=True)


def gotostock():
    root.destroy()
    sp.call('stock.py', shell=True)


def gotoadditem():
    root.destroy()
    sp.call('additem.py', shell=True)


def gotodisplay():
    root.destroy()
    sp.call('display.py', shell=True)

def gotoedit():
    root.destroy()
    sp.call('edit.py', shell=True)


def gotobill():
    root.destroy()
    sp.call('bill.py', shell=True)


def close():
    root.destroy()
    exit(0)


b1 = Button(root, text='Add Product', command=gotoadditem)
b1.config(font=('helvetica bold', 20), width=14)
b1.place(x=75, y=50)
b2 = Button(root, text='Stock', command=gotostock)
b2.config(font=('helvetica bold', 20), width=14)
b2.place(x=75, y=125)
b3 = Button(root, text='Issue', command=gotoissue)
b3.config(font=('helvetica bold', 20), width=14)
b3.place(x=75, y=200)
b4 = Button(root, text='Display Inventory', command=gotodisplay)
b4.config(font=('helvetica bold', 20), width=14)
b4.place(x=290, y=50)
b5 = Button(root, text='Edit', command=gotoedit)
b5.config(font=('helvetica bold', 20), width=14)
b5.place(x=290, y=125)
b6 = Button(root, text='Billing', command=gotobill)
b6.config(font=('helvetica bold', 20), width=14)
b6.place(x=290, y=200)
b7 = Button(root, text='Close', command=close)
b7.config(font=('helvetica bold', 8), width=6)
b7.place(x=540, y=10)

root.mainloop()
