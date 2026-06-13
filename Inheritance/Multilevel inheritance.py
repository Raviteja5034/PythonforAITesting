class A:
    x,y=10,20
    def methodA(self):
        print(self.x+self.y)
class B(A):
    a,b=40,50
    def methodB(self):
        print(self.a+self.b)
class C(B):
    i,j=60,70
    def methodC(self):
        print(self.i+self.j)
obj2=C()
obj2.methodA()
obj2.methodB()
obj2.methodC()

# 30
# 90
# 130