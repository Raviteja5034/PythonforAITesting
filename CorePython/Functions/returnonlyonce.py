class TestClass:
    def __init__(self, value,sample):
        self.value = value  # public variable 
        self.__sample=sample #private variable 

    def get_value(self):
        return self.value,self.__sample
        return self.__sample  # once return executed -it stopped immediately 
obj=TestClass(10,12)
output=obj.get_value()
print(output)

# (10, 12)