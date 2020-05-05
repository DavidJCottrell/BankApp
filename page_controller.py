import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
from tkinter import messagebox

#Super class for other page classes
class Page(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)

    def show(self):
        self.lift()

    def hide(self):
        self.lower()

#tk.Button wrapper classes to provide reusable custom button styles
class CustomSmallButton(tk.Button):
    def __init__(self, parent, *args, **kwargs):
        kwargs["width"] = 20
        tk.Button.__init__(self, parent, *args, **kwargs)
        self.parent = parent
class CustomLargeButton(tk.Button):
    def __init__(self, parent, *args, **kwargs):
        kwargs["width"] = 38
        tk.Button.__init__(self, parent, *args, **kwargs)
        self.parent = parent

#Import page classes
from login_page import LoginPage
from main_menu_page import MainMenuPage
from customer_options_page import CustomerOptMenuPage
from admin_options_page import AdminOptionsPage
from all_users_page import AllUsersPage


class PageController(tk.Frame):

    def __init__(self, root, bank_obj, middle_coords):

        tk.Frame.__init__(self)

        self.root = root

        self.bank_obj = bank_obj
        self.current_customer_account = None
        self.current_admin = None

        self.middle_coords = middle_coords

        self.pack(side="top", fill="both", expand = 1)
        
        PageContainer = tk.Frame(self)
        PageContainer.pack(side="top", fill="both", expand=True)

        page_list = []

        # Instantiate page classes
        self.loginPage = LoginPage(PageContainer, self, self.bank_obj)
        page_list.append(self.loginPage)

        self.mainMenuPage = MainMenuPage(PageContainer, self, self.bank_obj)
        page_list.append(self.mainMenuPage)

        self.custOptMenuPage = CustomerOptMenuPage(PageContainer, self, self.bank_obj)
        page_list.append(self.custOptMenuPage)

        self.adminOptionsPage = AdminOptionsPage(PageContainer, self, self.bank_obj)
        page_list.append(self.adminOptionsPage)

        self.showUsersPage = AllUsersPage(PageContainer, self, self.bank_obj)
        page_list.append(self.showUsersPage)

        for page in page_list:
            page.place(in_=PageContainer, x=0, y=0, relwidth=1, relheight=1)

        self.loginPage.show()
