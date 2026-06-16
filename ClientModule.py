import sys #sys is builtin module
sys.path.append("C:/Users/RavitejaPalakurthi/Documents/GitHub/Python/Package1")
import Module1,Module2
Module1.display()
Module2.show()
# This is module1 from Package1
# This is module2

from Package1.Module1 import display
display()
