import page_controller as pc

class MainMenuPage(pc.Page):
    def __init__(self, container, controller, bank_obj):
        pc.Page.__init__(self)
        self.controller = controller
        self.bank_obj = bank_obj

        self.bind("<<ShowMenu>>", self.on_show_frame)

        mainFrame = pc.tk.Frame(self)
        mainFrame.pack()

        self.AdminName_label = pc.tk.Label(mainFrame)
        self.AdminName_label.pack(pady=20)

        # Frame that contains buttons
        ButtonFrame = pc.tk.Frame(mainFrame)
        ButtonFrame.pack(pady=5)
        
        Transfer_btn = pc.CustomLargeButton(ButtonFrame, text="Transfer Money", command=self.Transfer)
        Transfer_btn.pack(pady=5)

        CUstOptions_btn = pc.CustomLargeButton(ButtonFrame, text="Customer account operations & profile settings", command=self.CustOptions)
        CUstOptions_btn.pack(pady=5)

        Del_btn = pc.CustomLargeButton(ButtonFrame, text="Delete customer", command=self.DeleteCustomer)
        Del_btn.pack(pady=5)

        Display_all_btn = pc.CustomLargeButton(ButtonFrame, text="Display all customer's details", command=self.PrintAllUsers)
        Display_all_btn.pack(pady=5)

        UpdateAdminInfo_btn = pc.CustomLargeButton(ButtonFrame, text="Update your details", command=self.ShowAdminOptions)
        UpdateAdminInfo_btn.pack(pady=5)

        ManagementReport_btn = pc.CustomLargeButton(ButtonFrame, text="Generate management report", command=self.GenManRep)
        ManagementReport_btn.pack(pady=5)

        SignOut_btn = pc.CustomLargeButton(ButtonFrame, text="Sign out", command=self.SignOut)
        SignOut_btn.pack(pady=5)
    
    def ShowAdminOptions(self):
        self.controller.mainMenuPage.hide()
        self.controller.adminOptionsPage.show()
    
    def on_show_frame(self, event):
        self.AdminName_label['text'] = "Welcome back " + self.controller.current_admin.fname + "!"
    
    def SignOut(self):
        self.controller.mainMenuPage.hide()
        self.controller.loginPage.show()
        self.controller.loginPage.event_generate("<<ShowLogin>>")
    
    def CustOptions(self):
        self.surname = pc.simpledialog.askstring("Input", "Enter customer's surname: ", parent=self)
        if self.surname == None:
            return
        self.controller.current_customer_account = self.bank_obj.search_customers_by_name(self.surname)
        if self.controller.current_customer_account != None:
            self.controller.mainMenuPage.hide()
            self.controller.custOptMenuPage.show()
            self.controller.custOptMenuPage.event_generate("<<ShowCustOpt>>")
        else:
            pc.messagebox.showinfo("error","Customer '" + self.surname + "' not found, please try again.")
            self.CustOptions()
    
    def PrintAllUsers(self):
        self.controller.mainMenuPage.hide()
        self.controller.showUsersPage.show()
        self.controller.showUsersPage.event_generate("<<ShowUsers>>")
    
    def DeleteCustomer(self):
        self.surname = pc.simpledialog.askstring("Input", "Enter surname of customer you want to delete: ", parent=self)
        if self.surname == None:
            return
        self.cust = self.bank_obj.search_customers_by_name(self.surname)
        if self.cust != None:
            self.bank_obj.accounts_list.remove(self.cust)
            pc.messagebox.showinfo("Success", self.surname + " was deleted.")
            self.bank_obj.update_file_with_deleted_customer(self.surname)
        else:
            pc.messagebox.showinfo("Error", self.surname + " was not found, please try again.")
            self.DeleteCustomer()
    
    def Transfer(self):

        #Get sender account
        while(True):
            sender_surname = pc.simpledialog.askstring("Input", "Enter the sender's surname: ", parent=self)
            if sender_surname == None:
                #User pressed cancel/didnt input anything
                return
            sender_obj = self.bank_obj.search_customers_by_name(sender_surname)
            if sender_obj == None:
                #Entered name is incorrect
                pc.messagebox.showinfo("error", "Customer not found, please try again.")
            else:
                break

        #Get sender account number
        while(True):
            sender_account_number = pc.simpledialog.askstring("Input", "Enter the sender's account number: ", parent=self)
            if sender_account_number == None:
                #User pressed cancel/didnt input anything
                return
            elif not sender_obj.check_account_number(sender_account_number):
                pc.messagebox.showinfo("error", "Account number not found, please try again.")
            else:
                break
        
        #Get receiver account
        while(True):
            receiver_surname = pc.simpledialog.askstring("Input", "Enter the receiver's surname: ", parent=self)
            if receiver_surname == None:
                #User pressed cancel/didnt input anything
                return
            receiver_obj = self.bank_obj.search_customers_by_name(receiver_surname)
            if receiver_obj == None:
                #Entered name is incorrect
                pc.messagebox.showinfo("error", "Customer not found, please try again.")
            else:
                break
        
        #Get sender account number
        while(True):
            receiver_account_number = pc.simpledialog.askstring("Input", "Enter the receiver's account number: ", parent=self)
            if receiver_account_number == None:
                #User pressed cancel/didnt input anything
                return
            elif not receiver_obj.check_account_number(receiver_account_number):
                pc.messagebox.showinfo("error", "Account number not found, please try again.")
            else:
                break

        #Get amount to send
        amount = pc.simpledialog.askstring("Input", "Enter amount to transfer: ", parent=self)
        if amount == None:
            #User pressed cancel/didnt input anything
            return
        
        #Make transfer
        if self.bank_obj.transferMoney(sender_surname, sender_account_number, receiver_surname, receiver_account_number, int(amount)):
            self.bank_obj.update_data()
            pc.messagebox.showinfo("Success", 
                "£" + amount + " has been successfully transferred from " + sender_obj.fname + " "
                + sender_obj.lname + " (account number: " + str(sender_account_number) + ") to " 
                + receiver_obj.fname + " " + receiver_obj.lname + " (account number: " + str(receiver_account_number) + ")"
                + "\n--------------------------------------------" 
                + "\n\n" + "Sender account number: " + str(sender_account_number) + " current balance is now £" + str(sender_obj.get_account_balance(sender_account_number))
                + "\n" + "Receiver account number: " + str(receiver_account_number) + " current balance is now £" + str(receiver_obj.get_account_balance(receiver_account_number))
            )
        else:
            pc.messagebox.showinfo("Error", "An error occured, please try again.")
    
    def GenManRep(self):
        pc.messagebox.showinfo("Management Report", 
                "Total customers: " + str(len(self.bank_obj.accounts_list)) + "\n"
                + "Total accounts used by customers: " + str(self.bank_obj.calc_total_number_of_accounts()) + "\n\n"
                + "Sum of all customer balances: £" + str(self.bank_obj.get_total_balances()) + "\n\n"
                + "Total interest to paid to customer's £" + str(self.bank_obj.calc_total_anual_interest()) + "\n\n"
                + "Total amount of overdrafts currently taken by all customers: £" + str(self.bank_obj.calc_all_used_overdrafts())
            )

