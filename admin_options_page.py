import page_controller as pc

class AdminOptionsPage(pc.Page):
    def __init__(self, container, controller, bank_obj):
        pc.Page.__init__(self)
        self.controller = controller
        self.bank_obj = bank_obj

        self.addr = []

        mainFrame = pc.tk.Frame(self, width=600, height=500)
        mainFrame.pack()

        ButtonFrame = pc.tk.Frame(mainFrame, height=100, width=100)
        ButtonFrame.pack(pady=50)

        UpdateName_btn = pc.CustomLargeButton(ButtonFrame, text="Update your name", command=self.UpdateName)
        UpdateName_btn.pack(pady=5)

        UpdateAddress_btn = pc.CustomLargeButton(ButtonFrame, text="Update your address", command=self.UpdateAddress)
        UpdateAddress_btn.pack(pady=5)

        UpdateUsername_btn = pc.CustomLargeButton(ButtonFrame, text="Update your username", command=self.UpdateUsername)
        UpdateUsername_btn.pack(pady=5)

        UpdatePassword_btn = pc.CustomLargeButton(ButtonFrame, text="Update your password", command=self.UpdatePassword)
        UpdatePassword_btn.pack(pady=5)
        
        ShowDetails_btn = pc.CustomLargeButton(ButtonFrame, text="Show your details", command=self.ShowDetails)
        ShowDetails_btn.pack(pady=5)

        Back_btn = pc.CustomLargeButton(ButtonFrame, text="Back", command=self.GoBack, width=38)
        Back_btn.pack(pady=5)
    
    def UpdateName(self):
        self.fname = pc.simpledialog.askstring("Input", "Enter new first name: ", parent=self)
        if self.fname != None:
                self.lname = pc.simpledialog.askstring("Input", "Enter new last name: ", parent=self)
                if self.lname != None:
                    self.controller.current_admin.update_first_name(self.fname)
                    self.controller.current_admin.update_last_name(self.lname)
                    self.bank_obj.update_data()
    
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
        
        self.controller.current_admin.update_address(self.addr)
        self.bank_obj.update_data()

    def ShowDetails(self):
        pc.messagebox.showinfo("Your details", 
              "First name: " + self.controller.current_admin.get_first_name() + "\n"
            + "Last name: " + self.controller.current_admin.get_last_name() + "\n\n"
            + "Full rights: " + str(self.controller.current_admin.has_full_admin_right()) + "\n\n"
            + "Address: " + str(self.controller.current_admin.address[0]) + "\n"
            + self.controller.current_admin.address[1] + "\n"
            + self.controller.current_admin.address[2] + "\n"
            + self.controller.current_admin.address[3] + "\n\n"
            + "Username: " + self.controller.current_admin.get_username() + "\n"
            + "Password: " + self.controller.current_admin.get_password()
        )

    
    def UpdateUsername(self):
        self.username = pc.simpledialog.askstring("Input", "Enter your new username: ", parent=self)
        if self.username == None:
            return
        self.controller.current_admin.set_username(self.username)
        self.bank_obj.update_data()
        pc.messagebox.showinfo("Success", "Your new username has been set.")
    
    def UpdatePassword(self):
        self.password = pc.simpledialog.askstring("Input", "Enter your new password: ", parent=self)
        if self.password == None:
            return
        self.controller.current_admin.update_password(self.password)
        self.bank_obj.update_data()
        pc.messagebox.showinfo("Success", "Your new password has been set.")
    
    def GoBack(self):
        self.controller.adminOptionsPage.hide()
        self.controller.mainMenuPage.show()