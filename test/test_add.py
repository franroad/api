# import os

# TEMP=os.getenv("TEMP") #IMPRIME UNA VARIABLE DE ENTORNO QUE EXISTE EN EL SISTEMA
# print(TEMP)

from app.calculations import add


def test_add():
    result=add(5,3)
    print(result)

# Calling the function test_add()
#not required for pytest