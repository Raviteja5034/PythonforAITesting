# slicing Technique 
lst=[10,20,30,40,50]
lst1=lst[: :]
print(f"lst values :{lst}")
print(f"lst1 values :{lst1}")

# lst values :[10, 20, 30, 40, 50]
# lst1 values :[10, 20, 30, 40, 50]

#Copy() function 
lst2=lst.copy()
print(f"lst2 values are:{lst2}")
# lst2 values are:[10, 20, 30, 40, 50]

#extend() function 
lst3=[90,100,200]
lst.extend(lst3)
print(f"lst4 values are:{lst}")
# lst4 values are:[10, 20, 30, 40, 50, 90, 100, 200]

#list() function 
lst5=list(lst3)
print(f"lst5 elements are:{lst5}")
# lst5 elements are:[90, 100, 200]