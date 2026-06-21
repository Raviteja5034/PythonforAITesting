num=int(input("Please enter number to check if it prime number or not"))
count=0 # declared variable to calculate how many factors are there for givennumber
if num>1: #check if num is greater than 1 or not 
    for i in range(1,num+1):    #assume num=5 range takes it 4 , so pls +1
         if num%i==0: #any numbers 1,2,3,4,5 is divided by 5 then count it 
              count=count+1
if count==2:
     print(f"{num} is the Price number as it has {count} factors")
else:
    print(f"{num} is the not a Price number as it has {count} factors")

# Please enter number to check if it prime number or not 19
# 19 is the Price number as it has 2 factors
# Please enter number to check if it prime number or not 20
# 20 is the not a Price number as it has 6 factors