from tkinter import *
from tkinter import messagebox
import subprocess as sp
import mysql.connector
from functools import partial

root4 = Tk()
root4.title('Edit')
root4.geometry('430x380')

conn = mysql.connector.connect(user='root', password='password', host='localhost', database='mydb')
mycursor = conn.cursor()

def gotohome():
    root4.destroy()
    sp.call('home.py', shell = True)

def clear_text():
    ecmob.delete(0, END)
    idbox.delete(0, END)
    tprice.delete(0, END)
    tquant.delete(0, END)
    tbatch.delete(0, END)

def editPrice(
    getcmobile,
    getid,
    getprice
    ):
    if not txt.get() or not txt1.get() or not txt2.get():
        messagebox.showerror('Error!!', 'Enter Valid Entries!!')
        clear_text()
        return
    id = getid.get()
    price = getprice.get()
    cmobile = getcmobile.get()
    if len(cmobile) != 10:
        messagebox.showerror('Error!!', 'Mobile Number should have 10 digits only')
        ecmob.delete(0, END)
        return
    mycursor.execute('SELECT iid FROM inventory WHERE iproductid = ' + id + ' AND cmobile = ' + cmobile)
    test = mycursor.fetchall()
    try:
        t = test[0][0]
    except:
        messagebox.showerror('Error!!', 'Product Doesn\'t Exist in Inventory!')
        clear_text()
        return
    try:
        mycursor.execute('UPDATE inventory SET iprice = ' + price + ' WHERE iproductid = ' + id + ' AND cmobile = ' + cmobile)
        messagebox.showinfo('Success!!', 'Edited Successfully!!')
        conn.commit()
    except:
        messagebox.showerror('Error!!', 'Error During Transaction!!')
        print(sys.exc_info()[0])
        clear_text()
        conn.rollback()
        return
    clear_text()


def editQuantity(
    getcmobile,
    getid,
    getquantity,
    getbatch
    ):
    if not txt.get() or not txt1.get() or not txt3.get() or not txt4.get():
        messagebox.showerror('Error!!', 'Enter Valid Entries!!')
        clear_text()
        return
    id = getid.get()
    quantity = getquantity.get()
    cmobile = getcmobile.get()
    ibatch = getbatch.get()
    if len(cmobile) != 10:
        messagebox.showerror('Error!!', 'Mobile Number should have 10 digits only')
        ecmob.delete(0, END)
        return
    mycursor.execute('SELECT iid FROM inventory WHERE iproductid = ' + id + ' AND cmobile = ' + cmobile + ' AND ibatch = ' + ibatch)
    test = mycursor.fetchall()
    if test is None:
        messagebox.showerror('Error!!', 'Product Doesn\'t Exist in Inventory!')
        clear_text()
        return
    try:
        mycursor.execute('UPDATE inventory SET iquantity = ' + quantity + ' WHERE iproductid = ' + id + ' AND cmobile = ' + cmobile + ' AND ibatch = ' + ibatch)
    except:
        messagebox.showerror('Error!!', 'Error During Transaction!!')
        print(sys.exc_info()[0])
        clear_text()
        conn.rollback()
        return
    messagebox.showinfo('Success!!', 'Edited Successfully!!')
    conn.commit()
    clear_text()


txt = StringVar()
txt1 = StringVar()
txt2 = StringVar()
txt3 = StringVar()
txt4 = StringVar()
lcmob = Label(root4, text='Enter Mobile No.')
lcmob.place(x=75, y=50)
ecmob = Entry(root4, textvariable=txt)
ecmob.place(x=200, y=50)
lid = Label(root4, text='Enter Product ID')
lid.place(x=75, y=75)
idbox = Entry(root4, textvariable=txt1)
idbox.place(x=200, y=75)
lprice = Label(root4, text='Enter New Price')
lprice.place(x=75,y=100)
tprice = Entry(root4, textvariable=txt2, width = 18)
tprice.place(x = 75, y = 125)
lquant = Label(root4, text='Enter Quantity')
lquant.place(x=200, y=100)
tquant = Entry(root4, textvariable=txt3, width = 14)
tquant.place(x=200, y=125)
lbatch = Label(root4, text='Enter Batch')
lbatch.place(x=290, y=100)
tbatch = Entry(root4, textvariable=txt4, width = 11)
tbatch.place(x=290, y=125)

editprice = partial(editPrice, txt, txt1, txt2)
editquantity = partial(editQuantity, txt, txt1, txt3, txt4)

editprice = Button(root4, text='Edit Price', command = editprice)
editprice.place(x = 100, y = 150)
editquant = Button(root4, text='Edit Quantity', command = editquantity)
editquant.place(x = 220, y = 150)

back = Button(root4, text='<-', command=gotohome)
back.place(x=10, y=10)
root4.mainloop()
conn.close()