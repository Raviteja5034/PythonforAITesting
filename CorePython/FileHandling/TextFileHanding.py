#writting data into text files
File=open("C:/Users/RavitejaPalakurthi/Documents/Archive/TextFileforPython.txt","w")
File.write("This is writing data into textfile \n")
File.write("This is writing data into textfile2")
File.close()

#Reading data from text file
File=open("C:/Users/RavitejaPalakurthi/Documents/Archive/TextFileforPython.txt","r")
print(File.read())
File.close()

# This is writing data into textfile
# This is writing data into textfile2

#Appending the data from text file
File=open("C:/Users/RavitejaPalakurthi/Documents/Archive/TextFileforPython.txt","a")
File.write("This is writting data into textfile3")
File.close()