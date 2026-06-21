
num1=int(input("Enter first number: "))
num2=int(input("Enter second number"))
# temp=num1
# num1=num2          # approach 1
# num2=temp
num1,num2=num2,num1 #appraoch 2
print(f"After swapping \n num1 is :{num1} \n num2 is :{num2} ")

# output -
# Enter first number: 100
# Enter second number 200
# After swapping 
#  num1 is :200 
#  num2 is :100 
