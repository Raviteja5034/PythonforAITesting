#Clear() function
lst=[6,0,4,1]
print(f"before clearing :{lst}")
lst.clear()
print(f"After clearning :{lst}")
# before clearing :[6, 0, 4, 1]
# After clearning :[]

# empty list []
lst1=[1,2,3,5]
print(f"before clearing :{lst1}")
lst1=[]
print(f"After clearning :{lst1}")

# before clearing :[1, 2, 3, 5]
# After clearning :[]

# *=0 
lst2 =[3,4,5,6]
print(f"before clearing :{lst2}")
lst2 *=0
print(f"After clearning :{lst2}")

# before clearing :[3, 4, 5, 6]
# After clearning :[]

#del function 
lst3=[4,8,9,1]
print(f"before clearing :{lst3}")
del lst3[:]
print(f"After clearning :{lst3}")

# before clearing :[4, 8, 9, 1]
# After clearning :[]