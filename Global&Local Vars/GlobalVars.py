global_Var=100  #global Var

def displayNum():
    local_var=200
    print(local_var)  #Local var available with in fubction
    print(global_Var) #global var available anywhere in program

displayNum()  # 200  100
