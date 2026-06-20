lst= list(map(int,input("Enter the List Items").split(",")))
sum=0
for i in range(len(lst)):
    if i%2==0:
        sum=sum+lst[i]
print(f"The sum of even numbers in {lst} are:{sum}")
