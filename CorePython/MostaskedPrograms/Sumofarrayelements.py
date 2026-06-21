lst=[1,2,3,4,5]
sum=0
for var in lst:
    sum=sum+var
print(f"sum of array elements:{sum}")
#direct method 
total=sum(lst)
print(total)
print(sum(total,10))
print(sum(total,-5))

