# import os

# TEMP=os.getenv("TEMP") #IMPRIME UNA VARIABLE DE ENTORNO QUE EXISTE EN EL SISTEMA
# print(TEMP)
import pytest
from app.calculations import add,substract,bank_account

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
    result=bank_account(50) #instance the function and send a value for __init__
    assert result.balance==50 #as we initialize with result , result is self outside the class
def test_bank_default_balance():
    result=bank_account()
    assert result.balance==0
# The same above but with parameters
@pytest.mark.parametrize("balance1, expected_balance",[
    (50,50),
    (0,0)

])
def test_balance_param(balance1,expected_balance):
    result=bank_account(balance1)
    assert result.balance==expected_balance
