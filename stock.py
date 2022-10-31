#!/usr/bin/python
# -*- coding: utf-8 -*-
from tkinter import *
import subprocess as sp
from tkinter import messagebox
import mysql.connector
from functools import partial
from datetime import datetime

root2 = Tk()
root2.title('Stock')
root2.geometry('430x380')

conn = mysql.connector.connect(user='root', password='password', host='localhost', database='mydb')
mycursor = conn.cursor()
now = datetime.now()
dts = now.strftime('%y-%m-%d %H:%M:%S')


def getBatch(getid):
    mycursor.execute('SELECT max(ibatch) FROM inventory WHERE iproductid = '+ getid)
    myresult = mycursor.fetchall()
    if myresult[0][0] is None:
        return 0
    return myresult[0][0]


def stock(
    getid,
    getquantity,
    getcmobile,
    ):
    if not txt.get() or not txt1.get() or not txt3.get():
        messagebox.showerror('Error!!', 'Enter Valid Entries!!')
        clear_text()
        return
    id = getid.get()
    get = int(getBatch(id))
    cmobile = getcmobile.get()
    if len(cmobile) != 10:
        messagebox.showerror('Error!!', 'Mobile Number should have 10 digits only')
        ecmob.delete(0, END)
        return
    batch = get + 1
    quantity = int(getquantity.get())
    try:
        mycursor.execute('SELECT itype,iname,iprice,sum(iquantity),cname FROM inventory WHERE iproductid = '
                          + id + ' AND cmobile = ' + cmobile)
        myresult = mycursor.fetchall()
        type = myresult[0][0]
        name = myresult[0][1]
        price = myresult[0][2]
        total = myresult[0][3] + quantity
        cname = myresult[0][4]
    except:
        messagebox.showerror('Error!!', 'Product Does not Exist!!')
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
        total,
        batch,
        'Stock',
        cname,
        cmobile,
        )
    try:
        mycursor.execute(sql, val)
        conn.commit()
    except:
        messagebox.showerror('Error!!', 'Error during Stocking!!')
        conn.rollback()
        return

    cursor = conn.cursor()
    sql = """INSERT INTO inventory(
       iproductid, iname, ibatch, iprice, iquantity, itype, cname, cmobile)
       VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
    val = (
        id,
        name,
        batch,
        price,
        quantity,
        type,
        cname,
        cmobile,
        )
    try:
        cursor.execute(sql, val)
        msg = 'Successfully!! Added ' + str(quantity) + ' units of ' + name
        messagebox.showinfo('Stocked Successfully', msg)
        conn.commit()
    except:
        messagebox.showerror('Error!!', 'Error during Registering!!')
        conn.rollback()

    clear_text()


def clear_text():
    idbox.delete(0, END)
    quant.delete(0, END)
    ecmob.delete(0, END)


def gotohome():
    root2.destroy()
    sp.call('home.py', shell=True)


def gotoadd():
    root2.destroy()
    sp.call('additem.py', shell=True)


txt = StringVar()
txt1 = StringVar()
txt3 = StringVar()
lcmob = Label(root2, text='Enter Mobile No.')
lcmob.place(x=100, y=50)
ecmob = Entry(root2, textvariable=txt3)
ecmob.place(x=200, y=50)
lid = Label(root2, text='Enter Product ID')
lid.place(x=100, y=75)
idbox = Entry(root2, textvariable=txt)
idbox.place(x=200, y=75)
lquant = Label(root2, text='Enter Quantity')
lquant.place(x=100, y=100)
quant = Entry(root2, textvariable=txt1)
quant.place(x=200, y=100)
stock = partial(stock, txt, txt1, txt3)
submit = Button(root2, text='Stock', command=stock)
submit.place(x=200, y=125)
clear = Button(root2, text='Clear', command=clear_text)
clear.place(x=250, y=125)
back = Button(root2, text='<-', command=gotohome)
back.place(x=10, y=10)

root2.mainloop()
conn.close()
