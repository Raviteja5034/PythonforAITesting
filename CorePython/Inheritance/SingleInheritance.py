class ClassA:
    def method1(self):
        print("This method1 from ClassA")

class ClassB(ClassA): #ClassA is Parent Class and Class B will child Class
    def method2(self):
        print("This method2 from ClassB")

Obj1=ClassB()
Obj1.method1() #This method1 from ClassA
Obj1.method2() #This method2 from ClassB

class A:
    x,y=10,20
    def methodA(self):
        print(self.x+self.y)
class B(A):
    a,b=40,50
    def methodB(self):
        print(self.a+self.b)
obj1=B()
obj1.methodA()
print(obj1.x,obj1.y)
obj1.methodB()
print(obj1.a,obj1.b)

# 30
# 10 20
# 90
# 40 50