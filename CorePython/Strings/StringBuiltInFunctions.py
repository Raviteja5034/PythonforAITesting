str="Raviteja"
#1.Concatenation
print(str+"Palakurthi") #RavitejaPalakurthi
#2.StringRepetation
print(str*3) #RavitejaRavitejaRaviteja
#3.Slicing
print(str[0:4]) #Ravi #starts with 0 and ending with 3 (4-1)
print(str[:4]) #Ravi #starts with 0 and ends with 4
print(str[4:]) #teja #starts with 4 and ends whole
print(str[0:-1]) # Ravitej # starts with 0 and ends with -1 leaving last element
#4.ord and chr
print(ord("R")) #82
print(chr(82)) # R
#5.min max len
print(max(str)) #V
print(min(str)) #R
print(max("RAVITEJA")) #V
print(min("RAVITEJA")) #A
print(max("Raviteja")) #v
print(min("Raviteja")) #R # Capital vales comes first for minimum
print(len(str)) #8
#6.in and not in
print("Ravi" in str) #True
print("Goud" in str) #False
print("Goud" not in str) #True
#7.String comparsions
print("Ravi"=="Ravi") #True
print("Ravi"!="ravi") #True
print("cd">"ab") #True #c comes late (bigger and a comes first(small)
#8.Testing string returns
str1="Raviteja123"
print(str1.isalnum())
print(str.isalpha())
print(str.isdigit())
print(str.isidentifier())
print(str.islower())
print("1/2".isnumeric())
#9.Search with substring
str2="Raviteja Palakurthi"
print(str2.startswith("Ravi"))
print(str2.endswith("Palakurthi"))
print(str2.count("R"))
print(str2.find("k"))
#10.Converting String
Str3="Welcome to python"
print(Str3.capitalize()) #Welcome to python
print(Str3.title()) #Welcome To Python
print(Str3.upper()) #WELCOME TO PYTHON
print(Str3.lower()) #welcome to python
print(Str3.swapcase()) #wELCOME TO PYTHON
print(Str3.replace("W","Z")) #Zelcome to python
Str4="  Raviteja  "
print(Str4.strip())
print(Str4.rstrip())
print(Str4.lstrip())
