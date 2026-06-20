ab=100

def display():
    ab=200
    print(ab)

display()  #200 as it refers to function ab ,not global ab
print(ab) #100 as it will print global ab as local ab is not available

#Global Variable can be declared inside the function with global keyword which can be
# used any where in the program
def display1():
    global xy
    xy=1000
    print(xy)

display1() #1000
print(xy) #1000

