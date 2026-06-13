class ClassA:
    x=100
    def displayA(self):
        x=10
        print("Method from Parent Class")

class ClassB(ClassA):
    def displayB(self):
        print("Method from Child Class")
        super().displayA()  #Class method accessing using super()
        print(super().x)  #Class Variable accessing using super()

mc=ClassB()
mc.displayB()
# Method from Child Class
# Method from Parent Class
#100
