print("This is Good1")
print("This is Good2")
try:
 print(10/2)  # ZeroDivisionError: division by zero
except ZeroDivisionError:
 print("Expection handled")
print("This Good3")

# This is Good2
# 5.0
# This Good3
