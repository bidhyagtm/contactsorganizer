"""
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    Final Project SDEV140
    Bidhya Gautam
    Application Name: Contact Organizer
    Version: 1.0
    Last Updated Date: 11/17/2022
    This application saves,edit or delete the contact information.
    Search functionality helps to search the existing record/s.
    This application uses SqlLite database to save the records.
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
"""

from tkinter import *
from tkinter import ttk
import sqlite3 #to create a table, I am using sqllite database
from tkinter import messagebox #to display the dialogbox 

#Creating dashboard window
class dashboard_window(Tk):
    def __init__(self): 
        super().__init__()
        self.configure(bg='#111')
        #setting window width and height
        self.canvas = Canvas(width=1280, height=720, bg='#e7e7e7')
        self.canvas.pack()
        self.maxsize(1280, 720)
        self.minsize(1280,720)
        self.state('zoomed')
        self.title('Contact Organizer')
        self.mymenu = Menu(self)
        #variable to store the search term to search contact
        search_term = StringVar() 

        #Application logo image
        self.logoImage = PhotoImage(file='images/pic-icon.png')
        self.logo = Label(self, image=self.logoImage, bg='#ffffff',text='Logo Image')
        self.logo.place(x=350, y=20)

        #creating table for contacts details view
        self.listTree = ttk.Treeview(self,height=20,columns=('First Name','Last Name','Company','Address','Contact Number','Secondary Contact Number','Email'))
        #vertical scrollbar
        self.vsb = ttk.Scrollbar(self,orient="vertical",command=self.listTree.yview)
        #horizontal scrollbar
        self.hsb = ttk.Scrollbar(self,orient="horizontal",command=self.listTree.xview)
        self.listTree.configure(yscrollcommand=self.vsb.set,xscrollcommand=self.hsb.set)
        self.listTree.heading("#0", text='ID')
        self.listTree.column("#0", width=50,minwidth=50,anchor='center')
        #defining the columns heading and its width
        self.listTree.heading("First Name", text='First Name')
        self.listTree.column("First Name", width=130, minwidth=100,anchor='center')
        self.listTree.heading("Last Name", text='Last Name')
        self.listTree.column("Last Name", width=130, minwidth=100,anchor='center')
        self.listTree.heading("Company", text='Company')
        self.listTree.column("Company", width=130, minwidth=100,anchor='center')
        self.listTree.heading("Address", text='Address')
        self.listTree.column("Address", width=250, minwidth=200, anchor='center')
        self.listTree.heading("Contact Number", text='Contact Number')
        self.listTree.column("Contact Number", width=100, minwidth=80, anchor='center')
        self.listTree.heading("Secondary Contact Number", text='Contact #2')
        self.listTree.column("Secondary Contact Number", width=100, minwidth=80, anchor='center')
        self.listTree.heading("Email", text='Email')
        self.listTree.column("Email", width=200, minwidth=150, anchor='center')
        self.listTree.place(x=80,y=250)
        self.vsb.place(x=1157,y=251,height=425)
        self.hsb.place(x=80,y=675,width=1075)
        ttk.Style().configure("Treeview",font=('Times new Roman',10))
        
        #Initialize database
        def initialize_database():
            conn = sqlite3.connect('ContactsDetails.db')
            with conn:
                cursor=conn.cursor()
                #Creating table if application is running first time
                cursor.execute('CREATE TABLE IF NOT EXISTS  tbl_Contacts_Record(FirstName Text,LastName Text,Company Text,Address Text,\
                                ContactNumber Text,SecondarContactNumber text,Email Text)')
                cursor.execute("select firstName from tbl_Contacts_Record") # get first name of all records
                if (len(cursor.fetchall())<1): #initialize table with one record if there is no data in table
                    cursor.execute('INSERT INTO tbl_Contacts_Record(FirstName,LastName,Company,Address,\
                                    ContactNumber,SecondarContactNumber,Email) VALUES(?,?,?,?,?,?,?)',
                                    ('Bidhya','Gautam','ABC Company','123 College Road, Lafayette, Indiana, 47905','1234567890','','bg@gmail.com'))
                
            conn.commit()
            cursor.close()
            conn.close()

        #list all the available contacts records
        def view_record():
            conn = sqlite3.connect('ContactsDetails.db')
            cursor = conn.cursor()

            cursor.execute("Select rowid,FirstName,LastName,Company,Address,\
                                ContactNumber,SecondarContactNumber,Email from tbl_Contacts_Record")
            pc = cursor.fetchall()
            if pc:
                self.listTree.delete(*self.listTree.get_children())
                for row in pc:
                    self.listTree.insert("",'end',text=row[0] ,values = (row[1],row[2],row[3],row[4],row[5],row[6],row[7]))
            else:
                messagebox.showinfo("Error", "No contacts found!")
            cursor.close()
            conn.close()
        
        #search record in the existing database
        def search_record():
            conn = sqlite3.connect('ContactsDetails.db')
            cursor = conn.cursor()
            cursor.execute("Select rowid,FirstName,LastName,Company,Address,\
                                ContactNumber,SecondarContactNumber,Email from tbl_Contacts_Record where FirstName like '%"+search_term.get()+"%' \
                                or LastName like '%"+search_term.get()+"%'")
            pc = cursor.fetchall()
            if pc:
                self.listTree.delete(*self.listTree.get_children())
                for row in pc:
                    self.listTree.insert("",'end',text=row[0] ,values = (row[1],row[2],row[3],row[4],row[5],row[6],row[7]))
            else:
                messagebox.showinfo("Error", "No record found!")
            cursor.close()
            conn.close()

        #Creating buttons and lables
        def display_action_buttons():
                    
                    #label and input box
                    self.label3 = Label(self, text='Contacts Organizer',fg='black' ,font=('Times new Roman', 30, 'bold'))
                    self.label3.place(x=420, y=22)
                    self.label6 = Label(self, text="Contacts Details",  font=('Times new Roman', 15, 'bold'))
                    self.label6.place(x=500, y=200)
                    #Creating the search box
                    self.label6 = Label(self, text="Name:",  font=('Times new Roman', 12))
                    self.label6.place(x=100, y=150)
                    self.entry_name = Entry(self,width = 20,textvariable = search_term)
                    self.entry_name.place(x = 150,y = 152)
                    self.button = Button(self, text='Search Contact',width=15, font=('Times new Roman', 10),command=search_record).place(x=280,y=148)

                    #Creating Action buttons
                    self.button = Button(self, text='Display Contact/s',width=25, font=('Times new Roman', 10),command=view_record).place(x=100,y=100)
                    self.button = Button(self, text='Add Contact', width=25, font=('Times new Roman', 10)).place(x=300,y=100)
                    self.button = Button(self, text="Update Contact", width=25, font=('Times new Roman', 10)).place(x=500, y=100)
                    self.button = Button(self, text="Delete Contact", width=25, font=('Times new Roman', 10)).place(x=700, y=100)
                    #application exit button
                    self.button = Button(self, text="Exit", width=25, font=('Times new Roman', 10),command=self.destroy).place(x=900, y=100)
                    
        display_action_buttons()
        initialize_database()

dashboard_window().mainloop()
