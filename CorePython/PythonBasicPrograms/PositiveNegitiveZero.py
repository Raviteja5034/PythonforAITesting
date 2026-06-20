
try:
    num=int(input("Please enter the number to check if it is even or odd"))
    if num>0:
      print(num,"is positive number")
    elif num<0:
     print(num,"is negitive number")
    else:
      print(num,"is zero")

except Exception as e1:
    print(e1)