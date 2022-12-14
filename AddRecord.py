#this module displaya the windows for add/edit contact records
#importing tkinter and other modules
from tkinter import *
from tkinter import ttk
import sys
import os
import sqlite3 #to create a table, I am using sqllite database
from tkinter import messagebox #to display the dialogbox 
from sqlite3 import Error
py = sys.executable

#creating window
class AddRecordWindow(Tk):
    def __init__(self):
        super().__init__()
        self.maxsize(600,500)
        self.minsize(600,500)
        self.title('Add Contact')
        self.canvas = Canvas(width=600, height=500, bg='#e7e7e7')
        self.canvas.pack()

        #Add Record image
        self.logoImage = PhotoImage(file='images/contact.png',width=70,height=50)
        self.logo = Label(self, image=self.logoImage, bg='#ffffff',text='Logo Image')
        self.logo.place(x=420, y=20)

        #defining variables to get the user's input
        fname = StringVar()
        lname = StringVar()
        companyName = StringVar()
        contact1 = StringVar()
        contact2 = StringVar()
        addressDetails = StringVar()
        emailId=StringVar()
        #validate data and save the record
        def save_record(save_edit_flag:BooleanVar):
                try:
                    self.conn = sqlite3.connect('ContactsDetails.db')
                    self.cursor = self.conn.cursor()
                    #getting the values from input fields
                    first = fname.get()
                    last = lname.get()
                    contactNumber = contact1.get()
                    secondaryContactNumber = contact2.get()
                    address = addressDetails.get()
                    email = emailId.get()
                    company=companyName.get()
                    #validating the users input
                    if(first=='' or last=='' or contactNumber==''):
                        if len(contactNumber)!=10:
                            messagebox.showerror("Error","Contact Number must 10 character long")
                        else:
                            messagebox.showerror("Error","Please provide the values in required fields")
                    else:
                        if save_edit_flag:#this for add recrod
                            self.cursor.execute('INSERT INTO tbl_Contacts_Record(FirstName,LastName,Company,Address,\
                                        ContactNumber,SecondaryContactNumber,Email) VALUES(?,?,?,?,?,?,?)',
                                        (first,last,company,address,contactNumber,secondaryContactNumber,email))
                            self.conn.commit()
                            #display the success message after record is saved
                        
                            messagebox.showinfo("Success","Record Saved Successfully")
                            #prompt user if they want to add more records or not
                            ask = messagebox.askyesno("Add more records","Do you want to add another contact information?")


                            if ask: #if user want to add more record then display the window
                                self.destroy()
                                os.system('%s %s' % (py, 'AddRecord.py'))
                            else: # close window and connection 
                                self.destroy()
                                self.cursor.close()
                                self.conn.close()

                        else:#this is for update the existing record
                            self.cursor.execute("UPDATE tbl_Contacts_Record set FirstName='"+first+"',LastName='"+last+"',"+
                                                            "Company='"+company+"',Address='"+address+"',ContactNumber='"+contactNumber+"',"+
                                                           "SecondaryContactNumber='"+secondaryContactNumber+"',Email='"+email+"' where rowid="+sys.argv[8]+"")
                            self.conn.commit()
                            #display the success message after record is updated
                        
                            messagebox.showinfo("Success","Record updated Successfully")
                            # close window and connection 
                            self.destroy()
                            self.cursor.close()
                            self.conn.close()
                        
                except Error:#if there is any error, display the message to the user
                    messagebox.showerror("Error","Failed to save record, please try again")
              

        # displaying the input fields for the users to get data
        Label(self, text='* indicates compulsory fields',font=('Times new Roman', 8, 'italic')).place(x=70,y=10)
        Label(self, text='*First Name:',  font=('Times new Roman', 10, 'bold')).place(x=70, y=60)
        Entry(self, textvariable=fname, width=30).place(x=200, y=62)
        Label(self, text='*Last Name:',  font=('Times new Roman', 10, 'bold')).place(x=70, y=110)
        Entry(self, textvariable=lname, width=30).place(x=200, y=112)
        Label(self, text='*Contact #:', font=('Times new Roman', 10, 'bold')).place(x=70, y=160)
        Entry(self, textvariable=contact1, width=20).place(x=200, y=162)
        Label(self, text='Secondary Contact #', font=('Times new Roman', 10, 'bold')).place(x=70, y=210)
        Entry(self, textvariable=contact2, width=20).place(x=200, y=212)
        Label(self, text='Company Name:', font=('Times new Roman', 10, 'bold')).place(x=70, y=260)
        Entry(self, textvariable=companyName, width=30).place(x=200, y=262)
        Label(self, text='Address:', font=('Times new Roman', 10, 'bold')).place(x=70, y=310)
        Entry(self, textvariable=addressDetails, width=50).place(x=200, y=312)
        Label(self, text='Email:', font=('Times new Roman', 10, 'bold')).place(x=70, y=360)
        Entry(self, textvariable=emailId, width=50).place(x=200, y=362)
        #save/edit button, display the caption based on user interaction i.e save or update
        if len(sys.argv)>1:
            Button(self, text="Update", width=15, command=lambda: save_record(False)).place(x=150, y=410)
        else:
            Button(self, text="Save", width=15, command=lambda: save_record(True)).place(x=150, y=410)
        #cancel or close button
        Button(self, text="Close", width=15, command=self.destroy).place(x=300, y=410)
        #sys.argv will be greater than one if this window is for edit record 
        #if windows is for edit record, show the existing information for the record in the form
        if(len(sys.argv)>1):
            fname.set(sys.argv[1])
            lname.set(sys.argv[2])
            companyName.set(sys.argv[3].replace('_###_','').replace('__',' '))
            #trimming the strings as we are passing the black if there is no data in the column
            contact1.set(sys.argv[5])
            contact2.set(sys.argv[6].replace('_###_',''))
            addressDetails.set(sys.argv[4].replace('_###_','').replace('__', ' '))
            emailId.set(sys.argv[7].replace('_###_',''))

AddRecordWindow().mainloop()
