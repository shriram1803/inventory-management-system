#!/usr/bin/python
# -*- coding: utf-8 -*-
from tkinter import *
import subprocess as sp
from tkinter import messagebox
import mysql.connector
from functools import partial
from datetime import datetime

root1 = Tk()
root1.title('Issue')
root1.geometry('430x380')

conn = mysql.connector.connect(user='root', password='password', host='localhost', database='mydb')
mycursor = conn.cursor()
now = datetime.now()
dts = now.strftime('%y-%m-%d %H:%M:%S')


def issue(
    getid,
    getquantity,
    getcmobile,
    ):
    if not txt.get() or not txt1.get() or not txt3.get():
        messagebox.showerror('Error!!', 'Enter Valid Entries!!')
        clear_text()
        return
    id = getid.get()
    quantity = int(getquantity.get())
    cmobile = getcmobile.get()
    if len(cmobile) != 10:
        messagebox.showerror('Error!!', 'Mobile Number should have 10 digits only')
        ecmob.delete(0, END)
        return
    tempquant = quantity
    name = ''
    price = 0
    cname = ''
    doregister = True
    while 1:
        try:
            mycursor.execute('SELECT iid,iquantity,iname,iprice,cname FROM inventory WHERE iproductid = '
                              + id +' AND ibatch = (SELECT MIN(ibatch) FROM inventory WHERE iproductid = '+id+') AND cmobile = '
                              + cmobile)
            myresult = mycursor.fetchall()
            gid = myresult[0][0]
            getquant = myresult[0][1]
            name = myresult[0][2]
            price = int(myresult[0][3])
            cname = myresult[0][4]
        except:
            messagebox.showerror('Error!!', 'Stock Not Available!!')
            doregister = False
            conn.rollback()
            break
        if quantity < getquant:
            newquantity = getquant - quantity
            mycursor.execute('UPDATE inventory SET iquantity = ' + str(newquantity) + ' WHERE iid = ' + str(gid))
            break
        elif quantity == getquant:
            mycursor.execute('DELETE FROM inventory WHERE iid = ' + str(gid))
            mycursor.execute('UPDATE inventory SET ibatch = ibatch - 1 WHERE iproductid = ' + str(id))
            break
        else:
            newquantity = quantity - getquant
            quantity = newquantity
            mycursor.execute('DELETE FROM inventory WHERE iid = ' + str(gid))
            mycursor.execute('UPDATE inventory SET ibatch = ibatch - 1 WHERE iproductid = ' + str(id))
    if doregister:
        try:
            mycursor.execute('SELECT sum(iquantity), max(ibatch) FROM inventory WHERE iproductid = ' + str(id))
            myresult = mycursor.fetchall()
            if myresult[0][0] is None:
                total = 0
                batch = 0
            else:
                total = int(myresult[0][0])
                batch = int(myresult[0][1])
            sql = """INSERT INTO register(dt, productid, productname, price, stockquant, issuequant, onhandquant, batches, process, cname, cmobile, payment)
                                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            val = (
                dts,
                id,
                name,
                price,
                0,
                tempquant,
                total,
                batch,
                'Issue',
                cname,
                cmobile,
                0
                )
            mycursor.execute(sql, val)
            msg = 'Successfully!! Issued ' + str(tempquant) + ' units of ' + name
            messagebox.showinfo('Issue Successful', msg)
        except:
            messagebox.showerror('Error!!', 'Error during Transaction!!')
            conn.rollback()

    conn.commit()
    clear_text()


def clear_text():
    idbox.delete(0, END)
    quant.delete(0, END)
    ecmob.delete(0, END)


def gotohome():
    root1.destroy()
    sp.call('home.py', shell=True)


txt = StringVar()
txt1 = StringVar()
txt3 = StringVar()
lcmob = Label(root1, text='Enter Mobile No.')
lcmob.place(x=100, y=50)
ecmob = Entry(root1, textvariable=txt3)
ecmob.place(x=200, y=50)
lid = Label(root1, text='Enter Product ID')
lid.place(x=100, y=75)
idbox = Entry(root1, textvariable=txt)
idbox.place(x=200, y=75)
lquant = Label(root1, text='Enter Quantity')
lquant.place(x=100, y=100)
quant = Entry(root1, textvariable=txt1)
quant.place(x=200, y=100)
issue = partial(issue, txt, txt1, txt3)
submit = Button(root1, text='Issue', command=issue)
submit.place(x=200, y=125)
clear = Button(root1, text='Clear', command=clear_text)
clear.place(x=250, y=125)
back = Button(root1, text='<-', command=gotohome)
back.place(x=10, y=10)

root1.mainloop()
conn.close()
