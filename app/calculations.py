def add(a:int,b:int):
    print('im in calculations')
    sum=a+b
    
    return sum 

def substract(a:int,b:int):
    
    subs=a-b
    
    
    return subs #not required for pytest

class bank_account:
    def __init__(self,starting_balance=0):
        self.balance=starting_balance
    
    def deposit(self,amount):
        self.balance+=amount #el += hace que se guardfe en self.balance la suma
        

