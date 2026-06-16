import ClassA,ClassB
obj1=ClassA.clsA()
obj1.display1()

obj2=ClassB.ClsB()
obj2.display2()

# //approach
from ClassA import clsA
from ClassB import ClsB

obj3=clsA()
obj3.display1()
obj4=ClsB()
obj4.display2()

#approach 3
from ClassA import *
from ClassB import *
obj5=clsA()
obj5.display1()


