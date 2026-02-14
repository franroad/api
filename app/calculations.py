def add(a:int,b:int):
    print('im in calculations')
    sum=a+b
    
    return sum 

def substract(a:int,b:int):
    
    subs=a-b
    
    
    return subs #not required for pytest

class InsuficcientFunds(Exception): #We are personalizing the Python exception for the RAISE.
    pass


class bank_account: 
    def __init__(self,starting_balance=0): #default value in case no value is provided
        self.balance=starting_balance # adding atrtibute to "balance" to the object
        print(f"Initial Amount: "+ str(self.balance)) # se imprime cada vez que se instancia la clase
    
    def deposit(self,amount=0):
        self.balance+=amount #el += hace que se guardfe en self.balance la suma
        print(self.balance)

    def withdraw(self,amount):
        if self.balance<amount:
            #print("Not enough cash")
            raise InsuficcientFunds("Not Enough Cash")
        else:
            self.balance-=amount

            print(f"New balance: {self.balance}")

    
    
    def interest(self):
        self.balance*=1.5
        print(self.balance)
        

