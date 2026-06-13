class myfirstClass:
    def method3(self):
        print("Method3")
    @staticmethod
    def methodstatic1(self,name):
        print("My name is",name)

obj2=myfirstClass()
obj2.method3() #Method3
obj2.methodstatic1("Test","Snithik") #My name is Snithik
#Calling Static method via object is not best practice
#To Call static method via object we need to pass self value as Parameter
myfirstClass.methodstatic1("Test","Varnika") #My name is Varnika