# import os

# TEMP=os.getenv("TEMP") #IMPRIME UNA VARIABLE DE ENTORNO QUE EXISTE EN EL SISTEMA
# print(TEMP)
import pytest
from app.calculations import add,substract

@pytest.mark.parametrize("num1, num2, expected",[
    (3,2,5),
    (7,1,8)
]) #Paremetrize, testing different values same function

def test_add(num1, num2, expected): #parametrize testing multiple values
    result=add(num1,num2)
    assert result==expected

def test_substract():
    result=substract(9,5)
    assert result==4 #assert used to confimr a given condition , not only that the function runs without errors.

    print(result)

# Calling the function test_add()
#not required for pytest
test_substract()