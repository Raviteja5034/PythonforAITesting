#Creating the class

class FirstClass:
    def method1(self):
        print("FirstMethod")
    def method2(self):
        print("SecondMethod")
    def displayName(self,name):
        print("My name is",name)

#Creating the object for the class

obj1=FirstClass()
obj1.method1()  #FirstMethod
obj1.method2()  #SecondMethod
obj1.displayName("Raviteja") #My name is Raviteja