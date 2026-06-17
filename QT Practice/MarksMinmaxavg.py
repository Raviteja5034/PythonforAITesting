def Studentmarks(d1):
 sum=0
 for values in d1.values():
    sum=sum+values
 print(sum,"is sum of marks")
 avg=sum/len(d1)
 print(avg,"is avg of marks")

 lts=list(d1.values())
 print(lts)
 max=lts[0]
 for var in lts:
    if var>max:
        max=var
 print(f"The minimum number is {max}")

 min=lts[0]
 for var1 in lts:
     if var1<min:
        min=var1
 print(f"The maximum number is {min}")

Studentmarks({"Ravi":100,"Teja":99,"Snithik":99,"Varnika":99})

# 397 is sum of marks
# 99.25 is avg of marks
# [100, 99, 99, 99]
# The minimum number is 100
# The maximum number is 99




