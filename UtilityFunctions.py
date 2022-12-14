#this module has utility functions like deleting the record, viewing the reccords
# and initializing the database connection

#delete the contact record by record id
def delete_record(self,messagebox):
    if self.selectedID==0:
        messagebox.showinfo("Alert","Please select the record to delete")
    else:
        d = messagebox.askyesno("Confirm", "Are you sure you want to delete the Contact?")
        if d:
            try:
                self.cursor = self.conn.cursor()
                self.cursor.execute("Delete from tbl_Contacts_Record where rowid="+str(self.selectedID))
                self.conn.commit()
                self.cursor.close()
                messagebox.showinfo("Success","Contact record deleted Successfully")
                #clear the value of contact field
                self.selectedID.set("")
                view_record(self,)
            except:
                messagebox.showerror("Error","Failed to delete the record, please try again")

#list all the available contacts records
def view_record(self,messagebox):
    #connecting to the database
    #conn = sqlite3.connect('ContactsDetails.db')
    cursor = self.conn.cursor()
    #getting all the existing records from database
    cursor.execute("Select rowid,FirstName,LastName,Company,Address,\
                        ContactNumber,SecondaryContactNumber,Email from tbl_Contacts_Record")
    pc = cursor.fetchall()
    if pc:
        #deleting the existing records of list
        self.listTree.delete(*self.listTree.get_children())
        #Adding the records from database to the list
        for row in pc:
            self.listTree.insert("",'end',text=row[0] ,values = (row[1],row[2],row[3],row[4],row[5],row[6],row[7]))
    else: #if there is no record, inform the user by displaying the messagebox
        messagebox.showinfo("Error", "No contacts found!")
    #closing cursor and connection
    cursor.close()
    #conn.close()

#Initialize database
def initialize_database(self,sqlite3):
    self.conn = sqlite3.connect('ContactsDetails.db')
    with self.conn:
        cursor=self.conn.cursor()
        #Creating table if application is running first time
        cursor.execute('CREATE TABLE IF NOT EXISTS  tbl_Contacts_Record(FirstName Text,LastName Text,Company Text,Address Text,\
                        ContactNumber Text,SecondaryContactNumber text,Email Text)')
        cursor.execute("select firstName from tbl_Contacts_Record") # get first name of all records
        if (len(cursor.fetchall())<1): #initialize table with one dummy record if there is no data in table
            cursor.execute('INSERT INTO tbl_Contacts_Record(FirstName,LastName,Company,Address,\
                            ContactNumber,SecondaryContactNumber,Email) VALUES(?,?,?,?,?,?,?)',
                            ('Bidhya','Gautam','ABC Company','123 College Road, Lafayette, Indiana, 47905','1234567890','','bg@gmail.com'))
                
    self.conn.commit()
    cursor.close()
    #conn.close()