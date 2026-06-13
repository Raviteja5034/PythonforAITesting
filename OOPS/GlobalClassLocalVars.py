a,b=10,20

class MysecondClass:
    x,y=30,40

    def method4(self,i,j):
        print("Method sum is:",i+j)
        print("Class sum is:",(self.x+self.y))
        print("global sum is:",a+b)

obj3=MysecondClass()
obj3.method4(10,20)

# Method sum is: 30
# Class sum is: 70
# global sum is: 30