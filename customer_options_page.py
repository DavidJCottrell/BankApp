import page_controller as pc

class CustomerOptMenuPage(pc.Page):
    def __init__(self, container, controller, bank_obj):
        pc.Page.__init__(self)
        self.controller = controller
        self.bank_obj = bank_obj

        self.bind("<<ShowCustOpt>>", self.on_show_frame)

        self.addr = []

        mainFrame = pc.tk.Frame(self, width=600, height=500)
        mainFrame.pack()

        self.CustomerName_label = pc.tk.Label(mainFrame)
        self.CustomerName_label.pack(pady=20)

        # Frame that contains buttons
        ButtonFrame = pc.tk.Frame(mainFrame, height=100, width=100)
        ButtonFrame.pack(pady=5, padx=50)

        Deposit_btn = pc.CustomLargeButton(ButtonFrame, text="Deposit Money", command=self.Deposit)
        Deposit_btn.pack(pady=5)

        Withdraw_btn = pc.CustomLargeButton(ButtonFrame, text="Withdraw Money", command=self.Withdraw)
        Withdraw_btn.pack(pady=5)

        Balance_btn = pc.CustomLargeButton(ButtonFrame, text="Check balance", command=self.ShowBalance)
        Balance_btn.pack(pady=5)

        UpdateName_btn = pc.CustomLargeButton(ButtonFrame, text="Update customer's name", command=self.UpdateName)
        UpdateName_btn.pack(pady=5)

        UpdateAddress_btn = pc.CustomLargeButton(ButtonFrame, text="Update customer's address", command=self.UpdateAddress)
        UpdateAddress_btn.pack(pady=5)
        
        ShowDetails_btn = pc.CustomLargeButton(ButtonFrame, text="Show customer's details", command=self.ShowDetails)
        ShowDetails_btn.pack(pady=5)

        Back_btn = pc.CustomLargeButton(ButtonFrame, text="Back", command=self.GoBack)
        Back_btn.pack(pady=5)
    
    def on_show_frame(self, event):
        self.CustomerName_label['text'] = "Options for customer " + self.controller.current_customer_account.fname + " " + self.controller.current_customer_account.lname + ":"

    def Deposit(self):
        amount = pc.simpledialog.askstring("Input", "Enter deposit amount: ", parent=self)
        if amount == None:
            return
        account_no = pc.simpledialog.askstring("Input", "Enter account number: ", parent=self)
        if account_no == None:
            return
        self.controller.current_customer_account.deposit(int(amount), account_no)
        self.bank_obj.update_data()
        pc.messagebox.showinfo("Success", "£" + str(amount) + " has been added to account " + str(account_no))

    def Withdraw(self):
        amount = pc.simpledialog.askstring("Input", "Enter amount to withdraw: ", parent=self)
        if amount == None:
            return
        account_no = pc.simpledialog.askstring("Input", "Enter account number: ", parent=self)
        if account_no == None:
            return
        if self.controller.current_customer_account.withdraw(int(amount), int(account_no)):
            self.bank_obj.update_data()
            pc.messagebox.showinfo("Success", "£" + str(amount) + " has been withdrawn from account " + str(account_no))
        else:
            pc.messagebox.showinfo("Error", "Insufficient funds, please try again")
            self.Withdraw()
    
    def ShowBalance(self):
        account_no = pc.simpledialog.askstring("Input", "Enter account number: ", parent=self)
        if account_no == None:
            return
        pc.messagebox.showinfo("Balance", 
            str(self.controller.current_customer_account.fname) + " " 
            + str(self.controller.current_customer_account.lname) + "'s balance for account number " 
            + str(account_no) + " is £" + str(self.controller.current_customer_account.get_account_balance(account_no))
        )
    
    def UpdateName(self):
        self.fname = pc.simpledialog.askstring("Input", "Enter new first name: ", parent=self)
        if self.fname != None:
                self.lname = pc.simpledialog.askstring("Input", "Enter new last name: ", parent=self)
                if self.lname != None:
                    self.controller.current_customer_account.update_first_name(self.fname)
                    self.controller.current_customer_account.update_last_name(self.lname)
                    self.bank_obj.update_data()
                    pc.messagebox.showinfo("Success", "Customer's name is now " + self.fname + " " + self.lname)

    def UpdateAddress(self):
        self.addr.append(pc.simpledialog.askstring("Input", "Enter new house number: ", parent=self))
        if self.addr[0] == None:
            return
        self.addr.append(pc.simpledialog.askstring("Input", "Enter new street name: ", parent=self))
        if self.addr[1] == None:
            return
        self.addr.append(pc.simpledialog.askstring("Input", "Enter new city name: ", parent=self))
        if self.addr[2] == None:
            return
        self.addr.append(pc.simpledialog.askstring("Input", "Enter new postcode: ", parent=self))
        if self.addr[3] == None:
            return

        for elem in self.addr: 
            if elem == None:
                return
        
        self.controller.current_customer_account.update_address(self.addr)
        self.bank_obj.update_data()
        pc.messagebox.showinfo("Success", "Customer's address was changed successfully")

    def ShowDetails(self):

        print(self.controller.current_customer_account.get_number_of_accounts())

        account_str = ""

        for account in self.controller.current_customer_account.accounts:
            account_str += "\nAccount number: " + str(account[0])
            account_str += "\n\tAccount type: " + str(account[1])
            account_str += "\n\tInterest rate: " + str(account[2])
            account_str += "\n\tBalance: " + str(account[3])
            account_str += "\n\tOverdraft limit: " + str(account[4]) + "\n"
        
        pc.messagebox.showinfo(self.controller.current_customer_account.fname + "'s details", 
              "First name: " + self.controller.current_customer_account.get_first_name() + "\n"
            + "Last name: " + self.controller.current_customer_account.get_last_name() + "\n"
            + "Address: " + str(self.controller.current_customer_account.address[0]) + "\n"
            + self.controller.current_customer_account.address[1] + "\n"
            + self.controller.current_customer_account.address[2] + "\n"
            + self.controller.current_customer_account.address[3] + "\n"
            + "\nAccounts:\n"
            + account_str
        )
    
    def GoBack(self):
        self.controller.custOptMenuPage.hide()
        self.controller.mainMenuPage.show()
