mydict1={100:"Raviteja",101:"Meghana",102:"Varnika",103:"Snithik"}

#accessing items from dict
print(mydict1[100],mydict1[101],mydict1[102],mydict1[103])
# Raviteja Meghana Varnika Snithik

mydict2={"First":"Banana","Second":"apple","Third":"Guava"}
print(mydict2["First"],mydict2["Second"],mydict2["Third"])
#Banana apple Guava

#Updating Dict Values :

mydict2["First"]="Kiwi"
mydict2["Second"]=2000
mydict2["Third"]=345.627
print(mydict2)
#{'First': 'Kiwi', 'Second': 2000, 'Third': 345.627}

#Printing Dict values :

for var in mydict2:
    print(var)
#Only keys printed
# First
# Second
# Third

for x in mydict2:
    print(mydict2[x])
#Only values printed
# Kiwi
# 2000
# 345.627

for keys in mydict2.keys():
    print(keys)
# First
# Second
# Third
for values in mydict2.values():
    print(values)
# Kiwi
# 2000
# 345.627
for keys,Values in mydict2.items():
    print(keys,values)
# First 345.627
# Second 345.627
# Third 345.627

#Length of dict
print(len(mydict2))  #3

#Substring checking
if "First" in mydict2:
    print("The First is available")
else:
    print("The First is not available") #The First is available

#Adding new item (key:value ) into Dict
mydict2["Fourth"]="Peddi"
print(mydict2)
#{'First': 'Kiwi', 'Second': 2000, 'Third': 345.627, 'Fourth': 'Peddi'}

#Removing Items from the dict
mydict2.pop("Third")
print(mydict2)
#{'First': 'Kiwi', 'Second': 2000, 'Fourth': 'Peddi'}

mydict1.clear()
print(mydict1)  # {}

#Copying from the dict
mydict3=mydict2.copy()
print(mydict3)
#{'First': 'Kiwi', 'Second': 2000, 'Fourth': 'Peddi'}