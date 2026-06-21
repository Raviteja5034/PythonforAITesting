lst=[10,20,30,10,40,50,10]

#print(lst.count(10)) # 3 
count=0
for var in lst:
    if var==10:
        count=count+1
print(f"The number of times 10 occured is: {count}")

# The number of times 10 occured is: 3