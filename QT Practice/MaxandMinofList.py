lst= list(map(int,input("Enter the List Items").split(",")))
min=lst[0]
for a in lst:
    if a<min:
        min=a
print(f"Minimum of {lst} is:{min}")
max=lst[len(lst)-1]
for b in lst:
    if b>max:
        max=b
print(f"Maximum of {lst} is:{max}")




