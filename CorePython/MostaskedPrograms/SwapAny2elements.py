lst=[23,65,19,90]

#approach 1 
lst[1],lst[3]=lst[3],lst[1]
print(f"List after exchanging:{lst}") #[23, 90, 19, 65]

#approach 2 
temp=lst[1]
lst[1]=lst[3]
lst[3]=temp
print(f"List after exchanging:{lst}") 

#approach 3 
Selement=lst.pop(1) 
Felement=lst.pop(2) # since 65 already removed -90 position is 2 now [23,19,90]
lst.insert(1,Selement)
lst.append(Felement)
print(f"List after exchanging:{lst}") 

# List after exchanging:[23, 65, 19, 90]