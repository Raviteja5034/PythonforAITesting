#List is collection used to multiple values of different data types in
#single Variable
#List represented with []
#List allows all data types & combinations of it
#List allows duplicates
#List are mutable
#List Index starts 0 to n and -1 to -n

#Creation of lists
list1=[10,20,30,40,50]
list2=["Ravi","Teja","Snithik","Meghana","Varnika"]
list3=[100,"Raju","Sita",200]
list4=list()
list5=[]

#Indexes of list
print(list1[0],list1[1],list1[2],list1[3],list1[4]) #10 20 30 40 50
print(list1[-1],list1[-2],list1[-3],list1[-4],list1[-5]) #50 40 30 20 10

#Slicing of list
print(list1[1:3]) #[20, 30]

#Updating List values
list1[0]=100
print(list1[0],list1[1],list1[2],list1[3],list1[4]) #100 20 30 40 50

#getting all list values
for x in list1:
    print(x)
# 100
# 20
# 30
# 40
# 50

#length of list
print(len(list1)) #5

#checking substring present in list
if "10" in list1:
    print("10 is available")
else:
    print("10 is not available") #10 is not available

#Adding items to the list

list1.append("5034")
print(list1) #[100, 20, 30, 40, 50, '5034']
list1.insert(1,"Ravi")
print(list1) #100, 'Ravi', 20, 30, 40, 50, '5034']

#removing items from the list

list1.pop()
print(list1) # 100, 'Ravi', 20, 30, 40, 50]
list1.pop(1)

del list1[0]

list1.clear()
print(list1) #[]


#Copying items from one list to other

list4=list(list2)
print(list4) #['Ravi', 'Teja', 'Snithik', 'Meghana', 'Varnika']

list5=list4.copy()
print(list5) #['Ravi', 'Teja', 'Snithik', 'Meghana', 'Varnika']

#Joining the list

list6=list4+list5
print(list6)
#['Ravi', 'Teja', 'Snithik', 'Meghana', 'Varnika', 'Ravi',
# 'Teja', 'Snithik', 'Meghana', 'Varnika']

list5.extend(list3)
print(list5)
#['Ravi', 'Teja', 'Snithik', 'Meghana', 'Varnika', 100, 'Raju', 'Sita', 200]

for var in list5:
    list6.append(var)
print(list6)