import page_controller as pc


class LoginPage(pc.Page):
    def __init__(self, container, controller, bank_obj):
        pc.Page.__init__(self)

        self.controller = controller
        self.bank_obj = bank_obj
        self.bind("<<ShowLogin>>", self.on_show_frame)

        # Frame that contains input and button frames
        mainFrame = pc.tk.Frame(self, width=600)
        mainFrame.pack(pady=80)

        # Frame that contains inputs
        InputFrame = pc.tk.Frame(mainFrame, width=500)
        InputFrame.pack(padx=50)

        # Frame that contains buttons
        ButtonFrame = pc.tk.Frame(mainFrame, width=100)
        ButtonFrame.pack(pady=15, padx=50)

        # Label and input for customer ID
        self.Username_label = pc.tk.Label(InputFrame, text="Enter your username: ")
        self.Username_label.grid(row=1, column=1)
        self.Username_entry = pc.tk.Entry(InputFrame)
        self.Username_entry.grid(row=1, column=2)

        # Label and input for password
        self.Password_label = pc.tk.Label(InputFrame, text="Enter your password: ")
        self.Password_label.grid(row=2, column=1)
        self.Password_entry = pc.tk.Entry(InputFrame)
        self.Password_entry.config(show="*")
        self.Password_entry.grid(row=2, column=2)

        # Add submit button to button frame
        submit_btn = pc.CustomSmallButton(ButtonFrame, text="Login", command=self.CheckDetails)
        submit_btn.pack()

        # Add back button to button frame
        quit_btn = pc.CustomSmallButton(ButtonFrame, text="Quit", command=self.controller.root.destroy)
        quit_btn.pack(pady=5)

    def CheckDetails(self):
        admin_obj = self.bank_obj.admin_login(self.Username_entry.get(), self.Password_entry.get())
        if(admin_obj != None):
            self.controller.loginPage.hide()
            self.controller.mainMenuPage.show()
            self.controller.current_admin = admin_obj
            self.controller.mainMenuPage.event_generate("<<ShowMenu>>")
        else:
            pc.messagebox.showinfo("Incorrect login details", "Username or password is incorrect, please try again.")
    
    def on_show_frame(self, event):
        #Clear entry boxes when signing out
        self.Username_entry.delete(0, 'end')
        self.Password_entry.delete(0, 'end')
