#print numbers until entered
num=int(input("Please enter number"))
for var in range(0,num):
    print(var)

#print even numbers until entered
num=int(input("Please enter number"))
for var in range(0,num):
    if var%2==0:
        print(var)