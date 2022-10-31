from tkinter import *
from tkinter import messagebox
import mysql.connector
from functools import partial
from datetime import datetime

try:
    conn = mysql.connector.connect(user='root', password='password', host='localhost', database='mydb')
    mycursor = conn.cursor()
except:
    print('DB connectivity unsuccessful!!!')
now = datetime.now()
dts = now.strftime('%y-%m-%d %H:%M:%S')

root = Tk()
root.title('Home Page')
root.geometry('600x350')

txt2 = StringVar()
txt3 = StringVar()
gid = StringVar()
gname = StringVar()
gprice = StringVar()
gquant = StringVar()
gtype = StringVar()


def Add(
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

def addItem():
    global root3
    root3 = Tk()
    root3.title('Add Item')
    root3.geometry('430x380')
    '''
    global txt2
    global txt3
    global gid
    global gname
    global gprice
    global gquant
    global gtype

    '''
    
    global lcname
    global ecname
    global ecmob
    global tid
    global tname
    global tprice
    global tquant
    
    lcname = Label(root3, text='Enter Name')
    lcname.place(x=80, y=50)
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
        Add,
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
    back = Button(root3, text='<-', command=root3.destroy)
    back.place(x=10, y=10)
    root3.mainloop()

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

b1 = Button(root, text='Add Product', command=addItem)
b1.config(font=('helvetica bold', 20), width=14)
b1.place(x=75, y=50)
b2 = Button(root, text='Stock', command=Add)
b2.config(font=('helvetica bold', 20), width=14)
b2.place(x=75, y=125)
b3 = Button(root, text='Issue', command=Add)
b3.config(font=('helvetica bold', 20), width=14)
b3.place(x=75, y=200)
b4 = Button(root, text='Display Inventory', command=Add)
b4.config(font=('helvetica bold', 20), width=14)
b4.place(x=290, y=50)
b5 = Button(root, text='Edit', command=Add)
b5.config(font=('helvetica bold', 20), width=14)
b5.place(x=290, y=125)
b6 = Button(root, text='Billing', command=Add)
b6.config(font=('helvetica bold', 20), width=14)
b6.place(x=290, y=200)
b7 = Button(root, text='Close', command=Add)
b7.config(font=('helvetica bold', 8), width=6)
b7.place(x=540, y=10)

root.mainloop()