from PracticePackage.Calculator1 import Calculator
import pytest
obj=Calculator()
assert obj.sum(10,20)==30
assert obj.substract(20,10)==10
assert obj.division(30,15)==2
assert obj.multiplication(5,2)==10
add=obj.sum(10,20)
sub=obj.substract(20,10)
divide=obj.division(30,15)
mul=obj.multiplication(30,15)
File=open("C:/Users/RavitejaPalakurthi/Documents/Archive/Calculator.txt",'w')
File.write(f"The sum is :{add} \n The Subtraction is:{sub} \n The Multiplication is :{mul} \n The division is :{divide}")
File.close()
File=open("C:/Users/RavitejaPalakurthi/Documents/Archive/Calculator.txt",'r')
FileRead=File.read()
assert "sum" in FileRead
assert "Sub" in FileRead
assert "Mul" in FileRead



