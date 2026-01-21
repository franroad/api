def add(a:int,b:int):
    print('im in calculations')
    sum=a+b
    
    assert sum==8
    return sum #not required for pytest

