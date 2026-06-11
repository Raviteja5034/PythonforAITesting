myset1={10,20,"Ravi","Teja",12.30,True,10,20}
print(myset1)
#{'Teja', True, 'Ravi', 20, 10, 12.3}
#Set is unordered and will not allow printing duplicates

for var in myset1:
    print(var)
# True
# 20
# Teja
# 10
# 12.3
# Ravi

if "Ravi" in myset1:
    print("Ravi is available")
else:
    print("Ravi is not available")

#Adding items to set:

myset1.add("Snithik")
print(myset1)
#{True, 'Snithik', 'Ravi', 'Teja', 20, 10, 12.3}

myset1.update(["Varnika","Meghana"]) #Pass as List
print(myset1)
# {'Varnika', True, 10, 12.3, 'Meghana', 'Teja', 20, 'Snithik', 'Ravi'}

#Removing values from set

myset1.remove(12.3)
print(myset1)
# {True, 'Meghana', 10, 20, 'Ravi', 'Snithik', 'Varnika', 'Teja'}
myset1.discard(50)
print(myset1)
#{True, 10, 'Snithik', 20, 'Teja', 'Ravi', 'Meghana', 'Varnika'}
myset1.discard(True)
print(myset1)
#{'Snithik', 10, 20, 'Ravi', 'Meghana', 'Teja', 'Varnika'}

myset2={"Swarupa","Parashuram"}
myset3=myset1.union(myset2)
print(myset3)
#{'Parashuram', 'Meghana', 10, 'Varnika', 'Snithik', 'Teja', 'Ravi', 20, 'Swarupa'}

myset4=myset1.copy()
print(myset4)
#{'Snithik', 'Teja', 20, 'Varnika', 'Meghana', 10, 'Ravi'}