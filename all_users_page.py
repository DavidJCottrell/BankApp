import page_controller as pc

class AllUsersPage(pc.Page):
    def __init__(self, container, controller, bank_obj):
        pc.Page.__init__(self)
        self.controller = controller
        self.bank_obj= bank_obj
        self.bind("<<ShowUsers>>", self.on_show_frame)

        mainFrame = pc.tk.Frame(self)
        mainFrame.pack(expand=True, fill=pc.tk.BOTH)

        self.NoticeLabel = pc.tk.Label(mainFrame, text="Select and left click an entry to edit customer details or account information.")
        self.NoticeLabel.pack(pady=20)

        self.tree = pc.ttk.Treeview(mainFrame)

        self.tree["columns"]=("one","two","three", "four", "five")
        
        self.tree.column("#0",      width=25)
        self.tree.column("one",     width=75)
        self.tree.column("two",     width=275)
        self.tree.column("three",   width=50)
        self.tree.column("four",    width=75)
        self.tree.column("five",    width=50)

        self.tree.heading("#0",     text="Row #")
        self.tree.heading("one",    text="Full Name")
        self.tree.heading("two",    text="Address")
        self.tree.heading("three",  text="Account #")
        self.tree.heading("four",   text="Account type")
        self.tree.heading("five",   text="Balance")

        self.tree.pack()

        self.tree.pack(fill='x', padx=5, pady=5)

        self.tree.bind("<Button-2>", self.OnLeftClick)

        Back_btn = pc.tk.Button(mainFrame, text="Back", command=self.GoBack, width=38)
        Back_btn.pack(pady=5)
    
    def on_show_frame(self, event):
        self.tree.delete(*self.tree.get_children())
        row = 1
        for customer in self.bank_obj.accounts_list:
            customer_row = self.tree.insert("", "end", text=str(row), values=(customer.fname + " " + customer.lname, str(customer.address[0]) + " " + customer.address[1] + ", " + customer.address[2] + ", " + customer.address[3], " ", " ", " "))
            row += 1
            for account in customer.accounts:
                self.tree.insert(customer_row, "end", text="---", values=("  ---", "---", str(account[0]), account[1], account[3] ))
    

    def OnLeftClick(self, event):

        entryIndex = self.tree.focus()
        if entryIndex == '': 
            pc.messagebox.showinfo("Error", "Select a row before left clicking.")
            return

        x = self.controller.middle_coords['X']
        y = self.controller.middle_coords['Y']

        # Set up window
        win = pc.tk.Toplevel()
        win.title("Edit Entry")
        win.attributes("-topmost", True)
        win.geometry("%dx%d+%d+%d" % (350, 250, x + 150, y + 100))

        values = self.tree.item(entryIndex)["values"]

        if self.tree.parent(entryIndex) != '':
            #Setup entry box
            AccountTypeLabel = pc.tk.Label(win, text = "Name: ")
            AccountTypeEntry = pc.tk.Entry(win, width=30)
            
            AccountTypeEntry.insert(0, values[3])

            AccountTypeLabel.grid(row = 0, column = 0)
            AccountTypeEntry.grid(row = 0, column = 1)

            #Setup buttons
            Ok_Button = pc.tk.Button(win, text = "Ok")
            Ok_Button.bind("<Button-1>", lambda e: self.UpdateAccount(self.tree, win, self.tree.parent(entryIndex), AccountTypeEntry.get(), values[2]))
            Ok_Button.grid(row = 3, column = 1)

        else:
            #Setup entry boxes
            NameLabel = pc.tk.Label(win, text = "Name: ")
            NameEntry = pc.tk.Entry(win, width=30)
            
            NameEntry.insert(0, values[0])

            NameLabel.grid(row = 0, column = 0)
            NameEntry.grid(row = 0, column = 1)

            AddressLabel = pc.tk.Label(win, text = "Address: ")
            AddressEntry = pc.tk.Entry(win, width=30)
            
            AddressEntry.insert(0, values[1])
            
            AddressLabel.grid(row = 1, column = 0)
            AddressEntry.grid(row = 1, column = 1)
            
            #Setup buttons
            Ok_Button = pc.tk.Button(win, text = "Ok")
            Ok_Button.bind("<Button-1>", lambda e: self.UpdateCustomer(self.tree, win, NameEntry.get(), AddressEntry.get()))
            Ok_Button.grid(row = 3, column = 1)

        Cancel_Button = pc.tk.Button(win, text = "Cancel")
        Cancel_Button.bind("<Button-1>", lambda c: win.destroy())
        Cancel_Button.grid(row = 4, column = 1)

    
    def UpdateCustomer(self, tree, win, NameEntry, AddressEntry):

        #Check if any entry box is empty
        if len(NameEntry) == 0 or len(AddressEntry) == 0:
           pc.messagebox.showinfo("Error", "A field was left empty.")
           return

        #Get the clicked row number from the table
        AccountIndex = tree.index(tree.focus())

        #Update customer information in table
        tree.item(tree.focus(), text=str(AccountIndex+1), values = (NameEntry, AddressEntry, " ", " ", " "))

        #Format and store entry box information into their respective variables 
        new_first_name = NameEntry.split()[0] #Get first name from entry box
        new_last_name = NameEntry.split()[1] #Get last name from entry box

        chars_to_trim = len(AddressEntry.split()[0]) + 1 #Used to skip the house number (e.g. "14 ") when splitting by commas later
        new_addr = [] #Will contain the address parts from the entry box

        #Address from entry box is formatted like this: 14 Wilcot Street, Bath, B5 5RT
        new_house_number = AddressEntry.split()[0] #House number (split at spaces retrieves first word)
        new_addr.append(new_house_number) #Add house number to address list
        new_street = AddressEntry[chars_to_trim: ].split(', ')[0] #Street (First element after spliting at commas (skipping the house number))
        new_addr.append(new_street)
        new_city = AddressEntry[chars_to_trim: ].split(', ')[1] #City (second element after spliting at commas)
        new_addr.append(new_city)
        new_postcode = AddressEntry[chars_to_trim: ].split(', ')[2] #Postcode (third element after splitting at commas)
        new_addr.append(new_postcode)

        #Update customer object with new entry box information
        self.bank_obj.accounts_list[AccountIndex].update_first_name(new_first_name)
        self.bank_obj.accounts_list[AccountIndex].update_last_name(new_last_name)
        self.bank_obj.accounts_list[AccountIndex].update_address(new_addr)

        #Update the JSON file with the new data
        self.bank_obj.update_data()

        win.destroy()

        pc.messagebox.showinfo("Success", "Customer details updated successfully")
    
    def UpdateAccount(self, tree, win, parent_index, AccountType, AccountNo):
        #Check if any entry box is empty
        if len(AccountType) == 0:
           pc.messagebox.showinfo("Error", "Account type was left empty")
           return
        
        #Get the clicked row number from the table
        AccountIndex = tree.index(tree.focus())
        
        #Remove the old contents
        print(tree.focus())

        parent_customer = self.bank_obj.search_customer_by_account_number(AccountNo)

        InterestRate = self.bank_obj.get_interest_rate_by_account_type(AccountType)

        parent_customer.accounts[AccountIndex][1] = AccountType
        parent_customer.accounts[AccountIndex][2] = InterestRate

        tree.item(tree.focus(), text="---", values=("  ---", "---", str(parent_customer.accounts[AccountIndex][0]), parent_customer.accounts[AccountIndex][1], parent_customer.accounts[AccountIndex][3] ))

        #Update the JSON file with the new data
        self.bank_obj.update_data()

        win.destroy()

        pc.messagebox.showinfo("Success", "Account updated successfully")
    

    def GoBack(self):
        self.controller.showUsersPage.hide()
        self.controller.mainMenuPage.show()
    
