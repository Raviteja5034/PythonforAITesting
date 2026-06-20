#Polymorphism can be achieved with "Method Overloading "
class human():
    def sayHello(self,name=None):
        if name is not None:
            print("hello",name)
        else:
            print("hello")
h=human()
h.sayHello("Raviteja")
h.sayHello()
# hello Raviteja
# hello

# This is Polymorphism
#One method works in 2 different ways
#This is also called method overloading 