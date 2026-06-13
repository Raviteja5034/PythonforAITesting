class Bank:
    def RateofInt(self):
        return 0
class bankX(Bank):
    def RateofInt(self):
        return 1.1
class bankY(Bank):
    def RateofInt(self):
        return 2.2
objx=bankX()
print(objx.RateofInt())  # 1.1
objy=bankY()
print(objy.RateofInt())  #2.2
