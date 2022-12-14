"""
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    Final Project SDEV140
    Bidhya Gautam
    Application Name: Contact Organizer
    Version: 1.0
    This application saves,edit or delete the contact information.
    Search functionality helps to search the existing record/s.
    This application uses SqlLite database to save the records.
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
"""

from tkinter import *
from tkinter import ttk
import sqlite3 #to create a table, I am using sqllite database
from tkinter import messagebox #to display the dialogbox 
import os
import sys
from types import NoneType
import UtilityFunctions
py=sys.executable
#Creating dashboard window
class DashboardWindow(Tk):
    def __init__(self): 
        super().__init__()
        self.configure(bg='#111')
        #setting window width and height
        self.canvas = Canvas(width=1280, height=720, bg='#e7e7e7')
        self.canvas.pack()
        #declaring a variable for connection
        self.conn=NoneType
        
        #application title
        self.title('Contact Organizer')
        self.mymenu = Menu(self)
        #variable to store the search term to search contact
        search_term = StringVar() 
        #array variable to store the value of selected row
        self.row_data=[]
        #variable to store the the record ID
        self.selectedID=""
        
        #Application logo image
        self.logoImage = PhotoImage(file='images/pic-icon.png')
        self.logo = Label(self, image=self.logoImage, bg='#ffffff',text='Logo Image')
        self.logo.place(x=350, y=20)
        
        #function to retrieve the current selected row
        def select_item(a):
            currentRow = self.listTree.focus()
            rowValues=self.listTree.item(currentRow,'values')
            #saving selected row values in row_data variable
            self.row_data=rowValues
            self.selectedID=self.listTree.item(currentRow,'text')


        #creating table for contacts details view
        self.listTree = ttk.Treeview(self,height=20,columns=('First Name','Last Name','Company','Address','Contact Number','Secondary Contact Number','Email'))
        #vertical scrollbar
        self.vsb = ttk.Scrollbar(self,orient="vertical",command=self.listTree.yview)
        #horizontal scrollbar
        self.hsb = ttk.Scrollbar(self,orient="horizontal",command=self.listTree.xview)
        self.listTree.configure(yscrollcommand=self.vsb.set,xscrollcommand=self.hsb.set)
        self.listTree.heading("#0", text='ID')
        self.listTree.column("#0", width=50,minwidth=50,anchor='center')
        #defining the columns heading and its width of the list view
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
        self.listTree.bind('<ButtonRelease-1>', select_item)
        self.vsb.place(x=1157,y=251,height=425)
        self.hsb.place(x=80,y=675,width=1075)
        ttk.Style().configure("Treeview",font=('Times new Roman',10))

        #open a new window to save/edit the contact information based on parameter
        #add_edit_flag variable determine whether the record needs to be added or edited
        #true is for edit otherwise add
        def add_record(add_edit_flag:BooleanVar):
            if add_edit_flag:#edit the selected row record
                if len(self.row_data)>0: #row is selected and has data in it
                    #os.system('%s %s' % (py,'AddRecord.py',self.row_data)) self.row_data[0],self.row_data[1],self.row_data[2],self.row_data[3],
                                                              #self.row_data[4],self.row_data[5],self.row_data[6]
                    #using replace function to convert the space in the address text by __ as it is send as arguments to AddRecord file, it needs to be one word
                    #otherwise address with space will become the parameter for the file.
                    #passing the "_###_" if data is not in the corresponding column as all the data are not compulsary to the save record form
                    os.system('{} {} {} {} {} {} {} {} {} {}'.format(py,'AddRecord.py',self.row_data[0],self.row_data[1],
                                                              self.row_data[2].replace(' ','__') if len(self.row_data[2])>0 else '_###_',
                                                              self.row_data[3].replace(' ','__') if len(self.row_data[3])>0 else '_###_',
                                                              self.row_data[4],
                                                              self.row_data[5] if len(self.row_data[5])>0 else '_###_',
                                                              self.row_data[6] if len(self.row_data[6])>0 else '_###_',self.selectedID))
                else:#no row is selected, inform user
                    messagebox.showinfo("Alert", "Please select the record to edit from the display contacts list")
            else:#add new contact information
                os.system('%s %s' % (py,'AddRecord.py'))
        
       
        #list all the available contacts records
        def view_record():
            UtilityFunctions.view_record(self,messagebox)
           
        
        #search record in the existing database
        def search_record():
            #conn = sqlite3.connect('ContactsDetails.db')
            cursor = self.conn.cursor()
            #search query for the data in the database 
            cursor.execute("Select rowid,FirstName,LastName,Company,Address,\
                                ContactNumber,SecondaryContactNumber,Email from tbl_Contacts_Record where FirstName like '%"+search_term.get()+"%' \
                                or LastName like '%"+search_term.get()+"%'")
            pc = cursor.fetchall()
            if pc:
                self.listTree.delete(*self.listTree.get_children())
                for row in pc:
                    self.listTree.insert("",'end',text=row[0] ,values = (row[1],row[2],row[3],row[4],row[5],row[6],row[7]))
            else:
                messagebox.showinfo("Error", "No record found!")
            cursor.close()
            #conn.close()

        def delete_record():
            UtilityFunctions.delete_record(self,messagebox)

        #exit program
        def quit_program():
            if self.conn:
                self.conn.close()
            self.destroy()

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

                    #Creating Action buttons with callback function
                    #Display list of contact button
                    self.button = Button(self, text='Display Contact/s',width=25, font=('Times new Roman', 10),command=view_record).place(x=100,y=100)
                    #Add button opens the new window to add the contact information
                    #I am using lambda to send the data to callback function
                    self.button = Button(self, text='Add Contact', width=25, font=('Times new Roman', 10),command=lambda: add_record(False)).place(x=300,y=100)
                    #update button the new window to update the contact information
                    self.button = Button(self, text="Update Contact", width=25, font=('Times new Roman', 10),command=lambda: add_record(True)).place(x=500, y=100)
                    #delete button prompts the user to get confirmation for deletion
                    self.button = Button(self, text="Delete Contact", width=25, font=('Times new Roman', 10),command=delete_record).place(x=700, y=100)
                    #application exit button
                    self.button = Button(self, text="Exit", width=25, font=('Times new Roman', 10),command=quit_program).place(x=900, y=100)
                    
        display_action_buttons()
        UtilityFunctions.initialize_database(self,sqlite3)

DashboardWindow().mainloop()
