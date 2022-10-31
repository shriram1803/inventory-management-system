
import tkinter as tk
from tkinter import ttk
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
 
LARGEFONT =("Verdana", 35)
  
class tkinterApp(tk.Tk):
     
    # __init__ function for class tkinterApp
    def __init__(self, *args, **kwargs):
         
        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)
         
        # creating a container
        container = tk.Frame(self) 
        container.pack(side = "top", fill = "both", expand = True)
  
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
  
        # initializing frames to an empty array
        self.frames = {} 
  
        # iterating through a tuple consisting
        # of the different page layouts
        for F in (HomePage, Page1, Page2, Issue):
  
            frame = F(container, self)
  
            # initializing frame of that object from
            # startpage, page1, page2 respectively with
            # for loop
            self.frames[F] = frame
  
            frame.grid(row = 0, column = 0, sticky ="nsew")
  
        self.show_frame(HomePage)
  
    # to display the current frame passed as
    # parameter
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
         
        b1 = ttk.Button(self, text='Add Product', command = lambda : controller.show_frame(Page2))
        b1.config(width=20)
        b1.grid(row = 0, column = 1, padx = 10, pady = 10)
        b2 = ttk.Button(self, text='Stock', command = lambda : controller.show_frame(Page2))
        b2.config(width=20)
        b2.grid(row = 1, column = 1, padx = 10, pady = 10)
        b3 = ttk.Button(self, text='Issue', command = lambda : controller.show_frame(Issue))
        b3.config(width=20)
        b3.grid(row = 2, column = 1, padx = 10, pady = 10)
        b4 = ttk.Button(self, text='Display Inventory', command = lambda : controller.show_frame(Page2))
        b4.config(width=20)
        b4.grid(row = 0, column = 3, padx = 10, pady = 10)
        b5 = ttk.Button(self, text='Edit', command = lambda : controller.show_frame(Page2))
        b5.config(width=20)
        b5.grid(row = 1, column = 3, padx = 10, pady = 10)
        b6 = ttk.Button(self, text='Billing', command = lambda : controller.show_frame(Page2))
        b6.config(width=20)
        b6.grid(row = 2, column = 3, padx = 10, pady = 10)
        b7 = ttk.Button(self, text='Close', command = lambda : controller.show_frame(Page2))
        b7.grid(row = 6, column = 2, padx = 10, pady = 10)



class Issue(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
               
        
        global ecmob
        global idbox
        global quant
        lcmob = ttk.Label(self, text='Enter Mobile No.')
        lcmob.grid(row = 0, column = 1, padx = 10, pady = 10) 
        ecmob = ttk.Entry(self)
        ecmob.grid(row = 0, column = 2, padx = 10, pady = 10)
        lid = ttk.Label(self, text='Enter Product ID')
        lid.grid(row = 1, column = 1, padx = 10, pady = 10)
        idbox = ttk.Entry(self)
        idbox.grid(row = 1, column = 2, padx = 10, pady = 10)
        lquant = ttk.Label(self, text='Enter Quantity')
        lquant.grid(row = 2, column = 1, padx = 10, pady = 10)
        quant = ttk.Entry(self)
        quant.grid(row = 2, column = 2, padx = 10, pady = 10)
        issue = partial(Issue, idbox, quant, ecmob)
        submit = ttk.Button(self, text='Issue', command = lambda : controller.show_frame(Page2))
        submit.grid(row = 3, column = 1, padx = 10, pady = 10)
        clear = ttk.Button(self, text='Clear', command = clear_text)
        clear.grid(row = 3, column = 2, padx = 10, pady = 10)
        back = ttk.Button(self, text='<-', command = lambda : controller.show_frame(Page2))
        back.grid(row = 4, column = 1, padx = 10, pady = 10)
    
    def clear_text(self):
        idbox.delete("1.0","end")
        quant.delete("1.0","end")
        ecmob.delete("1.0","end")

    def Issue(self, getid, getquantity, getcmobile):
        if not getid.get() or not getquantity.get() or not getcmobile.get():
            messagebox.showerror('Error!!', 'Enter Valid Entries!!')
            self.clear_text()
            return
        id = getid.get()
        quantity = int(getquantity.get())
        cmobile = getcmobile.get()
        if len(cmobile) != 10:
            messagebox.showerror('Error!!', 'Mobile Number should have 10 digits only')
            ecmob.delete("1.0","end")
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














































# first window frame startpage
  
class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
         
        # label of frame Layout 2
        label = ttk.Label(self, text ="Startpage", font = LARGEFONT)
         
        # putting the grid in its place by using
        # grid
        label.grid(row = 0, column = 4, padx = 10, pady = 10)
  
        button1 = ttk.Button(self, text ="Page 1",
        command = lambda : controller.show_frame(Page1))
     
        # putting the button in its place by
        # using grid
        button1.grid(row = 1, column = 1, padx = 10, pady = 10)
  
        ## button to show frame 2 with text layout2
        button2 = ttk.Button(self, text ="Page 2",
        command = lambda : controller.show_frame(Page2))
     
        # putting the button in its place by
        # using grid
        button2.grid(row = 2, column = 1, padx = 10, pady = 10)
  
          
  
  
# second window frame page1
class Page1(tk.Frame):
     
    def __init__(self, parent, controller):
         
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text ="Page 1", font = LARGEFONT)
        label.grid(row = 0, column = 4, padx = 10, pady = 10)
  
        # button to show frame 2 with text
        # layout2
        button1 = ttk.Button(self, text ="StartPage",
                            command = lambda : controller.show_frame(StartPage))
     
        # putting the button in its place
        # by using grid
        button1.grid(row = 1, column = 1, padx = 10, pady = 10)
  
        # button to show frame 2 with text
        # layout2
        button2 = ttk.Button(self, text ="Page 2",
                            command = lambda : controller.show_frame(Page2))
     
        # putting the button in its place by
        # using grid
        button2.grid(row = 2, column = 1, padx = 10, pady = 10)
  
  
  
  
# third window frame page2
class Page2(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text ="Page 2", font = LARGEFONT)
        label.grid(row = 0, column = 4, padx = 10, pady = 10)
  
        # button to show frame 2 with text
        # layout2
        button1 = ttk.Button(self, text ="Page 1",
                            command = lambda : controller.show_frame(Page1))
     
        # putting the button in its place by
        # using grid
        button1.grid(row = 1, column = 1, padx = 10, pady = 10)
  
        # button to show frame 3 with text
        # layout3
        button2 = ttk.Button(self, text ="Startpage",
                            command = lambda : controller.show_frame(StartPage))
     
        # putting the button in its place by
        # using grid
        button2.grid(row = 2, column = 1, padx = 10, pady = 10)
  
  
# Driver Code
app = tkinterApp()
app.mainloop()