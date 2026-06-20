lst=list(map(int,input("Please enter the list values").split(",")))
sum=0
count=0
for var in lst:
    if var%2==0:
        sum=sum+var
        count=count+1
print(f"The sum of even numbers are:{sum}")
print(count)
avg=sum/count
print(f"The average of even numbers are:{avg}")
# Please enter the list values 10 ,20, 30
# The sum of even numbers are:60
# 3
# The average of even numbers are:20.0
