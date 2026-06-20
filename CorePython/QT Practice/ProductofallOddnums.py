lst=list(map(int,input("Enter the list items").split(",")))
Product=1
for x in lst:
    if x%2!=0:
        Product=Product*x
print(f"The product of {lst} is:{Product}")
# Enter the list items 1,2,3,4
# The product of [1, 2, 3, 4] is:3

