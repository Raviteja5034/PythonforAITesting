class A:
    x,y=10,20
    def methodA(self):
        print(self.x+self.y)
class B:
    a,b=40,50
    def methodB(self):
        print(self.a+self.b)
class C(A,B):
    i,j=60,70
    def methodC(self):
        print(self.i+self.j)
obj1=C()
obj1.methodA()
obj1.methodB()
obj1.methodC()

# 30
# 90
# 130