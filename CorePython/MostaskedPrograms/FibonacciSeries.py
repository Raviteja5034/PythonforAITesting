#0 1 1 2 3 5.....
n=int(input("Enter the number till where you want Fibonacci series"))
n1=0
n2=1
print(n1)
for i in range(2,n+1):
    sum=n1+n2  # 0+1=1 
    # 0 1 1 2 3 5 8.......
    # 0(n1) 1(n2)  1(n1+n2)
    # 1(n1) 1(n+n2)-->(n2)
    n1=n2 
    n2=sum 
    print(sum," ",end="") 
 
# Enter the number till where you want Fibonacci series 10
# 0
# 1  2  3  5  8  13  21  34  55  