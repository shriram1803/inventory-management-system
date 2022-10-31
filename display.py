from tkinter import *
import mysql.connector
import subprocess as sp

gui = Tk()
gui.title('Display Inventory')
conn = mysql.connector.connect(user='root', password='password', host='localhost', database='mydb')
mycursor = conn.cursor()
lst = [('Product Id','Product Name','Units Available','Batches','Price per Unit(Rs.)','Total Value(Rs.)')]
mycursor.execute('SELECT iproductid,iname,sum(iquantity),max(ibatch),iprice,SUM(iquantity*iprice) FROM inventory GROUP BY iproductid')
temp = mycursor.fetchall()
lst = lst + temp

def home():
    gui.destroy()
    sp.call('home.py',shell=True)

# Table class
class Table:
    # Initialize a constructor
    def __init__(self, gui):
        # An approach for creating the table
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
        back = Button(gui, text='Home', command=home , width=12, bg='grey',fg='Black', font=('Arial', 12, 'bold'))
        back.grid(row=total_rows,column=0)

total_rows = len(lst)
total_columns = len(lst[0])

table = Table(gui)
gui.mainloop()
conn.close()