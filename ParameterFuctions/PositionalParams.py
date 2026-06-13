def positional(a,b):
    print(a,b)

positional(10,20) #Positional Parameters(order follows)

#default values for positional Params
def position1(a,b=20):
    print(a,b)

position1(100,200) #100 200 default value overiddden by 200
position1(100) #100 20

