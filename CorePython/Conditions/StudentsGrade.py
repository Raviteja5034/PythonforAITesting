name=input("Please enter student name")
marks=int(input("Please enter student marks"))
if marks>80:
    print(f"Congratulations..!{name}.You Passed the exam in A Grade")
elif marks>60 and marks<80:
    print(f"Good..!{name}.You Passed exam in B Grade")
elif marks>40 and marks<60:
    print(f"Not bad..!{name}.You Passed exam in C Grade")
else:
    print(f"Sorry..!.You Failed the exam.work hard take again")

# Please enter student name Raviteja
# Please enter student marks 90
# Congratulations..! Raviteja .You Passed the exam in A Grade

# Please enter student name Rajesh
# Please enter student marks 70
# Good..! Rajesh.You Passed exam in B Grade

# Please enter student name Raghu
# Please enter student marks 41
# Not bad..! Raghu.You Passed exam in C Grade

# Please enter student name Remo
# Please enter student marks 30
# Sorry..!.You Failed the exam.work hard take again