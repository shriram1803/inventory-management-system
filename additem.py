#!/usr/bin/python
# -*- coding: utf-8 -*-
from tkinter import *
import subprocess as sp
from tkinter import messagebox
import mysql.connector
from functools import partial
from datetime import datetime

root3 = Tk()
root3.title('Add Item')
root3.geometry('430x380')

conn = mysql.connector.connect(user='root', password='password', host='localhost', database='mydb')
mycursor = conn.cursor()
now = datetime.now()
dts = now.strftime('%y-%m-%d %H:%M:%S')


def clear_text():
    tid.delete(0, END)
    tname.delete(0, END)
    tprice.delete(0, END)
    tquant.delete(0, END)
    gtype.set('Choose Type')
    ecname.delete(0, END)
    ecmob.delete(0, END)


def gotohome():
    root3.destroy()
    sp.call('home.py', shell=True)


def add(
    getid,
    getname,
    getprice,
    getquant,
    gettype,
    getcname,
    getcmobile,
    ):
    if not gid.get() or not gname.get() or not gprice.get() or not gquant.get() or not txt2.get() or not txt3.get():
        messagebox.showerror('Error!!', 'Enter Valid Entries!!')
        clear_text()
        return
    id = getid.get()
    name = getname.get()
    price = float(getprice.get())
    quantity = int(getquant.get())
    itype = gettype.get()
    cname = getcname.get()
    cmobile = getcmobile.get()
    if len(cmobile) != 10:
        messagebox.showerror('Error!!', 'Mobile Number should have 10 digits only')
        ecmob.delete(0, END)
        return
    mycursor.execute('SELECT iid FROM inventory WHERE iproductid = '+ id)
    row = mycursor.fetchone()
    if row is not None:
        messagebox.showwarning('Warning!!', 'The Product already Exists\nNote: Go to Stocking!!')
        clear_text()
        return
    sql = """INSERT INTO register(
               dt, productid, productname, price, stockquant, issuequant, onhandquant, batches, process, cname, cmobile)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    val = (
        dts,
        id,
        name,
        price,
        quantity,
        0,
        quantity,
        1,
        'Stock',
        cname,
        cmobile,
        )
    try:
        mycursor.execute(sql, val)
        conn.commit()
    except:
        messagebox.showerror('Error!!', 'Error during Transaction!!')
        conn.rollback()

    cursor = conn.cursor()
    sql = """INSERT INTO inventory(
        iproductid, iname, ibatch, iprice, iquantity, itype, cname, cmobile)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
    val = (
        id,
        name,
        1,
        price,
        quantity,
        itype,
        cname,
        cmobile,
        )
    try:
        cursor.execute(sql, val)
        msg = 'Successfully!! Added ' + str(quantity) + ' units of ' + name
        messagebox.showinfo('Stocked Successfully', msg)
        clear_text()
        conn.commit()
    except:
        messagebox.showerror('Error!!', 'Error during Transaction!!')
        conn.rollback()

lcname = Label(root3, text='Enter Name')
lcname.place(x=80, y=50)
txt2 = StringVar()
ecname = Entry(root3, textvariable=txt2)
ecname.place(x=200, y=50)
lcmob = Label(root3, text='Enter Mobile No.')
lcmob.place(x=80, y=75)
txt3 = StringVar()
ecmob = Entry(root3, textvariable=txt3)
ecmob.place(x=200, y=75)
gid = StringVar()
lid = Label(root3, text='Enter Product ID')
lid.place(x=80, y=100)
tid = Entry(root3, textvariable=gid)
tid.place(x=200, y=100)
gname = StringVar()
lname = Label(root3, text='Enter Product Name')
lname.place(x=80, y=125)
tname = Entry(root3, textvariable=gname)
tname.place(x=200, y=125)
gprice = StringVar()
lprice = Label(root3, text='Enter Product Price')
lprice.place(x=80, y=150)
tprice = Entry(root3, textvariable=gprice)
tprice.place(x=200, y=150)
gquant = StringVar()
lquant = Label(root3, text='Enter Stock Quantity')
lquant.place(x=80, y=175)
tquant = Entry(root3, textvariable=gquant)
tquant.place(x=200, y=175)
gtype = StringVar()
gtype.set('Choose Type')
lst = ['Raw Material', 'Work in Progress', 'Finished Goods']
drop = OptionMenu(root3, gtype, *lst)
drop.place(x=200, y=200)

add = partial(
    add,
    gid,
    gname,
    gprice,
    gquant,
    gtype,
    txt2,
    txt3,
    )

submit = Button(root3, text='Stock', command=add)
submit.place(x=150, y=240)
clear = Button(root3, text='Clear', command=clear_text)
clear.place(x=200, y=240)
back = Button(root3, text='<-', command=gotohome)
back.place(x=10, y=10)
root3.mainloop()
conn.close()
