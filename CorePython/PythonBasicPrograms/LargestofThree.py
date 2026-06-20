num1=int(input("Please enter num1"))
num2=int(input("Please enter num2"))
num3=int(input("Please enter num3"))
if num1>num2 and num1>num3:
    print(f"{num1} is largest")
elif num2>num1 and num2>num3:
    print(f"{num2} is largest")
else:
    print(f"{num3} is largest")

biggest=max(num1,num2,num3)
print(biggest)