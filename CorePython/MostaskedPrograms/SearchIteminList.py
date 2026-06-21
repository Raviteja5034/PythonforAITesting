lst=[1,6,3,5,3,4]

#approach 1
flag=0
for var in lst:
    if var==5:
        print("element is found")
        flag=1
        break
if(flag==0):
  print("element not found")

# element is found 

#appriach 2 

if "5" in lst:
    print("element is found")
else:
    print("element is not found ")



