# import os

# TEMP=os.getenv("TEMP") #IMPRIME UNA VARIABLE DE ENTORNO QUE EXISTE EN EL SISTEMA
# print(TEMP)
import pytest
from app.calculations import add,substract,bank_account
#Fixture allows us to initializa a function so we dont need to do it in the function itself (pytest) and runs before the function itself
@pytest.fixture
def fix_zero_bank_account():
    return bank_account(0)

@pytest.fixture
def fix_bank_account():
    return bank_account(55)

@pytest.fixture
def fix_interest_account():
    #creating bank account with 60
    return bank_account(60)

@pytest.mark.parametrize("num1, num2, expected",[
    (3,2,5),
    (7,1,8)
]) #Paremetrize, testing different values same function

def test_add(num1, num2, expected): #parametrize testing multiple values
    
    assert add(num1,num2)==expected # En una linea pero no generamos variable par imprimir

def test_substract():
    result=substract(9,5)
    assert result==4 #assert used to confimr a given condition , not only that the function runs without errors.

    print(result)

# Calling the function test_add()
#not required for pytest


#Testing clases
def test_bank_set_initial_balance():
    account=bank_account(50) #instance the function and send a value for __init__
    assert account.balance==50 #as we initialize with result , result is self outside the class
def test_bank_default_balance():
    account=bank_account()
    assert account.balance==0
    #assert fix_zero_bank_account.balance==0
    #assert round(result.balance, 4)==0

def test_add_amount():
    account=bank_account()
    account.deposit(5)



def test_interest(fix_interest_account): #Using fixture we don't need to instance the class
    #result=bank_account(20)
    #result.interest()
    fix_interest_account.interest()
    assert fix_interest_account.balance==90


# The same above but with parameters
@pytest.mark.parametrize("balance1, expected_balance",[
    (50,50),
    (0,0)

])
def test_balance_param(balance1,expected_balance):
    account=bank_account(balance1)
    assert account.balance==expected_balance

# Fixture + Parameters:: 


@pytest.mark.parametrize("deposited, expected",[
    (50,75),
    (0,0)

])
def test_bank_account_operation(fix_zero_bank_account,deposited,expected):
    fix_zero_bank_account.deposit(deposited)
    fix_zero_bank_account.interest()
    assert fix_zero_bank_account.balance==expected



#test Exceptions (raise) Pytest detesct the exception and returns an error
def test_withdraw():
    account=bank_account(50)
    account.withdraw(52)

#With the fixture below we are initializing the bank account with 55, the fixture is defined above.
#This way we can catch provoked exception so it does not count as error for pytest ↓↓↓
#↓↓↓
def test_exception_withdraw(fix_bank_account):
    with pytest.raises(Exception): #With this we are saying ei! this should raise an exception. If so , the test is pased
        fix_bank_account.withdraw(200)


