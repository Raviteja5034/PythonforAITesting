#Tuples are immutable
#Once created , we cannot add/remove values from it
mytupple1=(10,20,"Ramu","Sita")
print(mytupple1[0],mytupple1[1],mytupple1[2],mytupple1[3])
#10 20 Ramu Sita
print(mytupple1[-1],mytupple1[-2],mytupple1[-3],mytupple1[-4])
#Sita Ramu 20 10

for var in mytupple1:
    print(var)
# 10
# 20
# Ramu
# Sita

print(len(mytupple1)) #4

if "10" in mytupple1:
    print("10 is present in tupple")
else:
    print("10 is not present in tupple")
#10 is not present in tupple

# mytupple1[0]=100
#TypeError: 'tuple' object does not support item assignment

# Since Tuples are immutable, changing tuple items is not possible.
# But we can update tuple items indirect way by converting tuple into List
# then we can update list items, then again convert back to tuple again.

mylist1=list(mytupple1)
print(mylist1) #[10, 20, 'Ramu', 'Sita']
mylist1[0]=100
print(mylist1) #[100, 20, 'Ramu', 'Sita']
mytupple1=tuple(mylist1)
print(mytupple1)
#(100, 20, 'Ramu', 'Sita')

#Copying the tuple

mytupple4=tuple(mytupple1)
print(mytupple4)
#(100, 20, 'Ramu', 'Sita')