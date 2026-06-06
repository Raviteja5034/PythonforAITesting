num1=int(input("Please enter number"))
num2=int(input("Please enter othernumber"))
print(f"Before swapping number1 is:{num1} and number2 is:{num2}")
num1=num2
num2=num1
num1,num2=num2,num1
print(f"After swapping number1 is:{num1} and number2 is:{num2}")