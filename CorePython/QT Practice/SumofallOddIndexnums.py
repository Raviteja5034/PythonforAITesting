lst= list(map(int,input("Enter the List Items").split(",")))
sum=0
for i in range(1,len(lst),2):
    if i%2!=0:
        sum=sum+lst[i]
print(f"The sum of odd numbers is: {sum}")
