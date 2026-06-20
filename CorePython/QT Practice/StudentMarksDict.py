def studentmarks(students_results):
    # Total marks of each student
    mmarks = 0
    emarks = 0
    smarks = 0
    for k in list(students_results.keys()):
        mmarks = mmarks + students_results[k]["maths"]
        emarks = emarks + students_results[k]["english"]
        smarks = smarks + students_results[k]["science"]

    print(f"Total maths marks are:{mmarks}")
    print(f"Total english marks are:{emarks}")
    print(f"Total science marks are:{smarks}")
    File = open("Studentmarks.txt", 'w')
    File.write(f"Total maths marks are:{mmarks} \n")
    File.write(f"Total english marks are:{emarks} \n")
    File.write(f"Total science marks are:{smarks} \n")
    File.close()

studentmarks({1:{"maths":10,"english":20,"science":30}})
