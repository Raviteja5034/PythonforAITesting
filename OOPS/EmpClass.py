class EmpClass:
    def __init__(self,Empid,EmpName,EmpSalary):
    #Constructor taking 3 variables and assign to class variables so that those
    #variables available across the class
       self.empid=Empid
       self.empName=EmpName
       self.empsal=EmpSalary
    def __str__(self):
        return (self.empName)  #Only String values will accepted

    def display(self):
     print(self.empid,self.empName,self.empsal)

obj=EmpClass(1020230,"Ravi","22LPA")
obj.display() #1020230 Ravi 22LPA
print(obj) #Ravi