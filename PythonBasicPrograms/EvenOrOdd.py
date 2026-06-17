
try:
  num = int(input("Please enter the number to check if it is even or odd"))
  if num%2==0:
    print(num, "is even number")
  else:
    print(num,"is odd number")
except Exception as e1:
    print("Exception occured")
    print(e1)