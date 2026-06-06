name=input("Please enter your name")
age=int(input("Please enter your age"))
if age>18:
    print("Congratulations!",name,"You are eligible for voting")
else:
    print("Sorry!",name,"your age is not sufficient,Please try",18-age,"year")

# Please enter your name Ramu
# Please enter your age 10
# Sorry!  Ramu your age is not sufficient,Please try 8 year

# Please enter your name Raviteja
# Please enter your age 33
# Congratulations!  Raviteja You are eligible for voting
