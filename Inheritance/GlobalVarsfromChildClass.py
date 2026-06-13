class A:
    x,y=10,20

class B(A):
    i,j=30,40
    def display(self,a,b):
        print(a,b)
        print(self.i,self.j)
        print(self.x,self.y)
obj=B()
obj.display(10,20)

# 10 20
# 30 40
# 10 20