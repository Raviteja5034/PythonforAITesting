class A:
    x,y=10,20
    def methodA(self):
        print(self.x+self.y)
class B(A):
    a,b=40,50
    def methodB(self):
        print(self.a+self.b)
class C(A):
    i,j=60,70
    def methodC(self):
        print(self.i+self.j)
obj1=C()
obj1.methodA()
obj1.methodC()
# 30
# 130
obj2=B()
obj2.methodA()
obj2.methodB()
# 30
# 90