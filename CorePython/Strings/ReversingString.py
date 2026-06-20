
#Method1
str="Raviteja"
revstr=""
for var in str:
    revstr=var+revstr  #R #aR #VaR #iVar
print("The Reversed String is :",revstr)
#The Reversed String is : ajetivaR

#Method2
revstr1=str[: : -1]
print("The Reversed String is",revstr1)
#The Reversed String is ajetivaR


