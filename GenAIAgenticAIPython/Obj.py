class TestClass:
    def __init__(self, value):
        self.value = value

    def get_value(self):
        return self.value
obj=TestClass(10)
print(obj.get_value())
