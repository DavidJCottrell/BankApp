class CustomerAccount:

    def __init__(self, fname, lname, address, accounts):
        self.fname = fname
        self.lname = lname
        self.address = address
        self.accounts = accounts
    
    def update_first_name(self, fname):
        self.fname = fname

    def update_last_name(self, lname):
        self.lname = lname

    def get_first_name(self):
        return self.fname

    def get_last_name(self):
        return self.lname

    def update_address(self, addr):
        self.address = addr

    def get_address(self):
        return self.address
    
    def get_account_type(self, account_no):
        for account in self.accounts:
            if account[0] == int(account_no):
                return account[1]
    
    def get_number_of_accounts(self):
        return len(self.accounts)
    
    def get_account_numbers(self):
        for account in self.accounts:
            return account[0]
    
    def get_account_types(self):
        for account in self.accounts:
            return account[1]
    
    def get_interest_rates(self):
        for account in self.accounts:
            return account[2]
    
    def get_account_balance(self, account_no):
        for account in self.accounts:
            if account[0] == int(account_no):
                return account[3]
    
    def check_account_number(self, account_no):
        for account in self.accounts:
            if account[0] == int(account_no):
                return True
        return False

    def update_account_type(self, account_type, account_no):
        for account in self.accounts:
            if account[0] == int(account_no):
                account[1] = account_type
                if account_type == "Savings":
                    account[2] = 0.05
                else:
                    account[2] = 0.02

    
    def get_overdraft_limits(self):
        overdrafts = []
        for account in self.accounts:
            overdrafts.append(account[4])
        return overdrafts

    def deposit(self, amount, account_no):
        for account in self.accounts:
            if account[0] == int(account_no):
                account[3] += amount
                return True
        return False

    def withdraw(self, amount, account_no):
        for account in self.accounts:
            if account[0] == int(account_no):
                if(account[3] - amount >= -1 * account[4]):
                    account[3] -= amount
                    return True
                else:
                    print("Insufficient funds")
                    return False
        print("account number not found")
    
    #
    """
    def print_balance(self):
        print("\n The account balance is %.2f" %self.balance)
    
    
    def account_menu(self):
        print ("\n Your Transaction Options Are:")
        print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print ("1) Deposit money")
        print ("2) Withdraw money")
        print ("3) Check balance")
        print ("4) Update customer name")
        print ("5) Update customer address")
        print ("6) Show customer details")
        print ("7) Back")
        print (" ")
        option = int(input ("Choose your option: "))
        return option
    
    def print_details(self):
        print("First name: %s" %self.fname)
        print("Last name: %s" %self.lname)
        #print("Account No: %s" %self.account_no)
        print("Address: %s" %self.address[0])
        print(" %s" %self.address[1])
        print(" %s" %self.address[2])
        print(" %s" %self.address[3])
        print(" ")
   
    def run_account_options(self):
        loop = 1
        while loop == 1:
            choice = self.account_menu()
            if choice == 1:
                #amount=float(input("\n Please enter amount to be deposited: "))
                #self.deposit(amount)
                self.print_balance()
            elif choice == 2:
                pass
            elif choice == 3:
                self.print_balance()
            elif choice == 4:
                fname=input("\n Enter new customer first name: ")
                self.update_first_name(fname)
                sname = input("\nEnter new customer last name: ")
                self.update_last_name(sname)
            elif choice == 5:
                addr = input("\nEnter new address: ")
                self.update_address(addr)
            elif choice == 6:
                self.print_details()
            elif choice == 7:
                loop = 0
        print ("\n Exit account operations")

    """