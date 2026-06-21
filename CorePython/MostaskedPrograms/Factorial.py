# 3!=3*2*1
# 1*1=1
# 1*2=2
# 2*3=6 

num=int(input("Please enter number to calcuate the factorial of it"))
constant=1
if num<0:
    print(f"Factorial does not exists")
elif num==0:
    print(f"factorial of {num} is: 0")
else:
    for i in range(1,num+1):
        constant=constant*i
    print(f"The Factorial of {num} is :{constant}")   
 

# Please enter number to calcuate the factorial of it 12
# The Factorial of 12 is :479001600
# Please enter number to calcuate the factorial of it-10
# Factorial does not exists
# Please enter number to calcuate the factorial of it0
# factorial of 0 is: 0