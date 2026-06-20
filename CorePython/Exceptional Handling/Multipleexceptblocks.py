try:
    num1, num2 = 10, 5
    division = num1 / num2
    print(division)
except ZeroDivisionError:
    print("Exception-ZeroDivisionError")
except SyntaxError:
    print("Exception-SyntaxError")
except:
    print("Unknown exception")
else:
    print("No exception")
finally:
    print("No exception ,send an email")