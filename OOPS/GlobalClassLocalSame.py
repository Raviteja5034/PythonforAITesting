a,b=1000,2000

class myclass4:
    a,b=100,200
    def method5(self,a,b):
        print("Local sum is",a+b)
        print("Class sum is",self.a+self.b)
        print("Global sum is",globals()["a"]+globals()["b"])
obj4=myclass4()
obj4.method5(10,20)

# Local sum is 30
# Class sum is 300
# Global sum is 3000