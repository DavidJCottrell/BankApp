from customer_account import CustomerAccount
from admin import Admin
import json

class BankSystem(object):
    def __init__(self):
        self.accounts_list = [] #Stores all customers
        self.admins_list = [] #Stores all admins
        self.load_bank_data() #Loads the stored information about customers and admins from data.json    

    #Instantiate customer objects from information stored in the data JSON file
    def load_bank_data(self):
        
        #Load saved json from file and store in variable
        with open("data.json") as data_file:
            self.data = json.load(data_file)
                
        #Load customers from Json
        for customer in self.data["customer"]:
            addr = [] #Used to store address as list to pass to CustomerAccount constructor
            addr.append(customer["address"]["number"])
            addr.append(customer["address"]["street"])
            addr.append(customer["address"]["town"])
            addr.append(customer["address"]["postcode"])

            account_list = []
            
            for account in customer["accounts"]:
                current_account = []
                current_account.append(account['account_number'])
                current_account.append(account['account_type'])
                current_account.append(account['interest_rate'])
                current_account.append(account['balance'])
                current_account.append(account['overdraft'])
                account_list.append(current_account)

            #Create instance of customer class from JSON object
            self.accounts_list.append( CustomerAccount(customer["first_name"], customer["last_name"], addr, account_list) )
        
        #Load admins from JSON
        for admin in self.data["admin"]:
            addr = [] #Used to store address as list to pass to Admin constructor
            addr.append(customer["address"]["number"])
            addr.append(customer["address"]["street"])
            addr.append(customer["address"]["town"])
            addr.append(customer["address"]["postcode"])
            #Create instance of customer admin from JSON object
            self.admins_list.append( Admin(admin["first_name"], admin["last_name"], addr,  admin["username"],  admin["password"],  admin["full_rights"]) )

    #Called everytime admin or customer data is changed
    def update_data(self):        
        #Replace customer JSON stored in variable with new data from customer objects
        i = 0
        for customer in self.accounts_list:
            self.data["customer"][i]["first_name"] = customer.fname
            self.data["customer"][i]["last_name"] = customer.lname
            self.data["customer"][i]["address"]["number"] = customer.address[0]
            self.data["customer"][i]["address"]["street"] = customer.address[1]
            self.data["customer"][i]["address"]["town"] = customer.address[2]
            self.data["customer"][i]["address"]["postcode"] = customer.address[3]

            c = 0

            for account in customer.accounts:
                self.data["customer"][i]["accounts"][c]["account_number"] = account[0]
                self.data["customer"][i]["accounts"][c]["account_type"] = account[1]
                self.data["customer"][i]["accounts"][c]["interest_rate"] = account[2]
                self.data["customer"][i]["accounts"][c]["balance"] = account[3]
                self.data["customer"][i]["accounts"][c]["overdraft"] = account[4]
                c += 1
            i += 1 
        

        
        #Replace admin JSON stored in variable with new data from admin objects
        i = 0
        for admin in self.admins_list:
            self.data["admin"][i]["first_name"] = admin.fname
            self.data["admin"][i]["last_name"] = admin.lname
            self.data["admin"][i]["address"]["number"] = admin.address[0]
            self.data["admin"][i]["address"]["street"] = admin.address[1]
            self.data["admin"][i]["address"]["town"] = admin.address[2]
            self.data["admin"][i]["address"]["postcode"] = admin.address[3]
            self.data["admin"][i]["username"] = admin.user_name
            self.data["admin"][i]["password"] = admin.password
            self.data["admin"][i]["full_rights"] = admin.full_admin_rights
            i += 1
        
        #Replace all JSON in data file with updated JSON variable
        with open("data.json", 'w', encoding='utf-8') as data_file:
            json.dump(self.data, data_file, ensure_ascii=False, indent=4)

    #Returns the interest rate for each account type
    def get_interest_rate_by_account_type(self, account_type):
        if(account_type == "Savings"):
            return 0.05
        elif(account_type == "Debit"):
            return 0.02
        else:
            return False

    #Calculates the total interest to be paid to customers
    def calc_total_anual_interest(self):
        total = 0
        for customer in self.accounts_list:
            for account in customer.accounts:
                #Interest is only paid to balances above overdraft
                if account[3] > 0:
                    total += account[2] * account[3]
        return total
    
    #Returns the total number of accounts used across all customers
    def calc_total_number_of_accounts(self):
        total = 0
        for customer in self.accounts_list:
            total += customer.get_number_of_accounts()
        return total

    #Gets total balances across all customer accounts in the system
    def get_total_balances(self):
        total = 0
        for customer in self.accounts_list:
            for account in customer.accounts:
                total += account[3]
        return total
    
    #Calculates the total amount of overdraft currently used across all customers
    def calc_all_used_overdrafts(self):
        total = 0
        for customer in self.accounts_list:
            for account in customer.accounts:
                if account[3] < 0:
                    total += abs(account[3])
        return total
    
    #Returns the customer that has the customer object with the account number specified
    def search_customer_by_account_number(self, account_no):
        for customer in self.accounts_list:
            for account in customer.accounts:
                if account[0] == int(account_no):
                    return customer

    #Returns the admin with the specified name if it is found
    def search_admins_by_name(self, admin_username):
        found_admin = None
        for a in self.admins_list:
            username = a.get_username()
            if username == admin_username:
                found_admin = a
                break
        if found_admin == None:
            print("\n The Admin %s does not exist! Try again...\n" %admin_username)
        return found_admin

    #Returns the customer with the specified name if it is found
    def search_customers_by_name(self, customer_lname):
        found_customer = None
        for a in self.accounts_list:
            username = a.get_last_name()
            if username == customer_lname:
                found_customer = a
                break
        if found_customer == None:
            print("\n The Admin %s does not exist! Try again...\n" %customer_lname)
        return found_customer

    #Withdraws money from account with sender_lname and deopists into account with receiver_lname
    def transferMoney(self, sender_lname, sender_account_no, receiver_lname, receiver_account_no, amount):
        sender_account = self.search_customers_by_name(sender_lname)
        receiver_account = self.search_customers_by_name(receiver_lname)
        #Returns false if the customer does not have enough money to make the withdrawal
        if sender_account.withdraw(amount, sender_account_no):
            receiver_account.deposit(amount, receiver_account_no)
            return True
        else:
            return False

    #Returns the admin with the specified username if it is found in the list of admins and the provided password is correct.
    def admin_login(self, username, password):
        found_admin = self.search_admins_by_name(username)
        if found_admin != None:
            if found_admin.get_password() == str(password):
                return found_admin

    def update_file_with_deleted_customer(self, surname):
        index = self.get_customer_file_index(surname)
        del self.data["customer"][index]
        # print(json.dumps(self.data, indent=4, sort_keys=True))
        with open("data.json", 'w', encoding='utf-8') as data_file:
            json.dump(self.data, data_file, ensure_ascii=False, indent=4)


    def get_customer_file_index(self, surname):
        counter = 0
        for customer in self.data["customer"]:
            if(customer["last_name"] == surname):
                return counter
            counter+=1

    """
    #NOT IN USE (PROVIDED FOR CLI)
    def main_menu(self):
        #print the options you have
        print()
        print()
        print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print ("Welcome to the Python Bank System")
        print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print ("1) Admin login")
        print ("2) Quit Python Bank System")
        print (" ")
        option = int(input ("Choose your option: "))
        return option
    
    #NOT IN USE (PROVIDED FOR CLI)
    def run_main_options(self):
        loop = 1
        while loop == 1:
            choice = self.main_menu()
            if choice == 1:
                username = input ("\n Please input admin username: ")
                password = input ("\n Please input admin password: ")
                msg, admin_obj = self.admin_login(username, password)
                print(msg)
                if admin_obj != None:
                    self.run_admin_options(admin_obj)
            elif choice == 2:
                loop = 0
        print ("\n Thank-You for stopping by the bank!")

    #NOT IN USE (USED FOR CLI)
    def admin_menu(self, admin_obj):
        #print the options you have
        print (" ")
        print ("Welcome Admin %s %s : Avilable options are:" %(admin_obj.get_first_name(), admin_obj.get_last_name()))
        print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print ("1) Transfer money")
        print ("2) Customer account operations & profile settings")
        print ("3) Delete customer")
        print ("4) Print all customers detail")
        print ("5) Sign out")
        print (" ")
        option = int(input ("Choose your option: "))
        return option

    #NOT IN USE (PROVIDED FOR CLI)
    def run_admin_options(self, admin_obj):                                
        loop = 1
        while loop == 1:
            choice = self.admin_menu(admin_obj)
            if choice == 1:
                sender_lname = input("\n Please input sender surname: ")
                amount = float(input("\n Please input the amount to be transferred: "))
                receiver_lname = input("\n Please input receiver surname: ")
                #receiver_account_no = input("\n Please input receiver account number: ")
                #self.transferMoney(sender_lname, receiver_lname, receiver_account_no, amount)
                self.transferMoney(sender_lname, receiver_lname, amount)         
            elif choice == 2:
                customer_name = input("\n Please input customer surname :\n")
                customer_account = self.search_customers_by_name(customer_name)
                if customer_account != None:
                    customer_account.run_account_options()
            
            elif choice == 3:
                customer_name = input("\n input customer name you want to delete: ")
                customer_account = self.search_customers_by_name(customer_name)
                if customer_account != None:
                    self.accounts_list.remove(customer_account)
                    print("%s was deleted successfully!" %customer_name)
            
            elif choice == 4:
                self.print_all_accounts_details()
                pass
            
            elif choice == 5:
                loop = 0
        print ("\n Exit account operations")

    #NOT IN USE (PROVIDED FOR CLI)
    def print_all_accounts_details(self):
            # list related operation - move to main.py
            i = 0
            for c in self.accounts_list:
                i+=1
                print('\n %d. ' %i, end = ' ')
                c.print_details()
                print("------------------------")


#NOT IN USE (PROVIDED FOR CLI)
#app = BankSystem()
#app.run_main_options()
"""