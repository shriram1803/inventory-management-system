from tkinter import *
import subprocess as sp
import  mysql.connector
from functools import partial
from tkinter import messagebox

bill = Tk()
bill.title('Bill')
bill.geometry('430x380')

conn = mysql.connector.connect(user='root', password='password', host='localhost', database='mydb')
mycursor = conn.cursor()

def gotohome():
    bill.destroy()
    sp.call('home.py', shell = True)

def displaybill(getcmobile):
    if not txt.get():
        messagebox.showerror('Error!!', 'Enter Valid Entry!!')
        clear_text()
        return
    cmobile = getcmobile.get()
    if len(cmobile) != 10:
        messagebox.showerror('Error!!', 'Mobile Number should have 10 digits only')
        ecmob.delete(0, END)
        return
    mycursor.execute('SELECT productid,dt,productname,price,issuequant,0.25*issuequant FROM register WHERE payment = false AND cmobile = ' + cmobile)
    res = mycursor.fetchall()
    try:
        r = res[0][0]
    except:
        messagebox.showinfo('', 'No Bills Currently Available!')
        clear_text()
        return
    rows = len(res)
    columns = len(res[0])
    lst = [('Product ID', 'Date', 'Product Name', 'Rate', 'Quantity', 'Price')]
    lst += res
    Table(lst, rows+1, columns)

class Table:
    # Initialize a constructor
    def __init__(self, l, r, c):
        # An approach for creating the table
        gui = Tk()
        gui.title('Bill')
        def exit_bill():
            gui.destroy()
        def doPayment(getmob):
            cmobile = getmob.get()
            try:
                curs = conn.cursor()
                qry = 'UPDATE register SET payment = true WHERE payment = false AND cmobile = ' + cmobile
                curs.execute(qry)
                conn.commit()
                messagebox.showinfo('Transaction', 'Your Transaction is Successful!!')
                gui.destroy()
                bill.destroy()
                sp.call('home.py', shell = True)
            except:
                messagebox.showerror('Error!!', 'Error During Transaction!!')
                print(sys.exc_info()[0])
                clear_text()
                conn.rollback()
                gui.destroy()
        total_rows = r
        total_columns = c
        lst = l
        tot = 0
        for i in range(1, total_rows):
            tot += float(lst[i][5])
        for i in range(total_rows):
            for j in range(total_columns):
                if i ==0:
                    self.entry = Entry(gui, width=14, bg='LightSteelBlue',fg='Black',
                                       font=('Arial', 12, 'bold'))
                else:
                    self.entry = Entry(gui, width=14, fg='blue',
                               font=('Arial', 12, ''))
                self.entry.grid(row=i, column=j)
                self.entry.insert(END, lst[i][j])
        back = Button(gui, text='Exit', command=exit_bill , width=12, bg='grey',fg='Black', font=('Arial', 12, 'bold'))
        back.grid(row=total_rows,column=0)
        pay = partial(doPayment, txt)
        back = Button(gui, text='Pay', command=pay, width=12, bg='grey', fg='Black', font=('Arial', 12, 'bold'))
        back.grid(row=total_rows, column=1)
        totalstr = 'Total Price = ' + str(tot)
        totaldsp = Label(gui, text = totalstr, width = 14, bg='grey', fg='black', font=('Arial',12,'bold'))
        totaldsp.grid(row = total_rows, column = 5)


def clear_text():
    ecmob.delete(0, END)

txt = StringVar()
lcmob = Label(bill, text='Enter Mobile No.')
lcmob.place(x=100, y=50)
ecmob = Entry(bill, textvariable=txt)
ecmob.place(x=200, y=50)
display = partial(displaybill, txt)
submit = Button(bill, text='Display', command=display)
submit.place(x=200, y=125)
clear = Button(bill, text='Clear', command=clear_text)
clear.place(x=250, y=125)
back = Button(bill, text='<-', command=gotohome)
back.place(x=10, y=10)

bill.mainloop()
conn.close()