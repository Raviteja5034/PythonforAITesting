def returnval(a,b):
    if a>b:
        return a,b
    else:
        return b,a

x,y=returnval(10,20)
print(x,y) #20 10