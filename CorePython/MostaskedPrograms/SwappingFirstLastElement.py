# # take a temp variable 
# # put 1st variable in temp variable
# # assign last variable to 1st variable
# # assign temp variable to last variable 
# #approach 1 
lst=[12,35,9,56,24]
temp=lst[0]
lst[0]=lst[len(lst)-1]
lst[len(lst)-1]=temp
print(f"after swapping :{lst}")

# #approach 2 
lst[0],lst[-1]=lst[-1],lst[0]
print(f"after swapping :{lst}")

#approach 3 
lst=[12,35,9,56,24]
start,*middle,end=lst
lst=[end,*middle,start]
print(lst)

#approach 4 
lst=[12,35,9,56,24]
firstelement=lst.pop(0) #removes 1st element
lastelement=lst.pop(-1) #removes the last element
lst.insert(0,lastelement)
lst.append(firstelement)
print(lst)

#[24, 35, 9, 56, 12]