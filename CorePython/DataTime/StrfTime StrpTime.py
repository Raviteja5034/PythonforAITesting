from datetime import datetime
#strftime()
now=datetime.now()
print(now) #2026-06-19 15:10:25.583641
print(now.strftime("%Y-%m-%d")) #2026-06-19
print(now.strftime("%y-%m-%d")) #26-06-19
print(now.strftime("%Y/%m/%d")) #2026/06/19
#strptime()
date="2026-05-19 15:30:00"
dateobj=datetime.strptime(date,"%Y-%m-%d %H:%M:%S") #2026-05-19 15:30:00
print(dateobj)
datenice=datetime.strftime(dateobj,"%d-%m-%Y")
print(datenice)
datenice=datetime.strftime(dateobj,"%B-%m-%Y")
print(datenice)