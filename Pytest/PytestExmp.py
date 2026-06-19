def add(a,b):
    sum=a+b
    division=a/b
    substraction=a-b
    multiplication=a*b
    return sum,division,substraction,multiplication

def test_add():
    assert add(10,5)==(15, 2.0, 5, 10)


