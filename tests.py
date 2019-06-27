#
# tests.py
#
# started this file and copied everthing seeming useful form my Jupyter Notebook


import pprint
import datetime
from datetime import timedelta
from datetime import date

import random
#import json
import re
#import csv

import TiTra


pp = pprint.PrettyPrinter(indent=2)

all_projects=dict()
all_task=dict()



def InitForTest(cal:TiTra.Calender):
    now=datetime.datetime.today()
    now=now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    mlater=now+timedelta(weeks=0, days=32, hours=0, minutes=0, seconds=0)  
    mlater=mlater.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    
    print (f"\n*** Actions löschen zwischen {now} und {now+timedelta(days=40)}")
    
    cal.removeBetween(now,now+timedelta(days=40))
    
    print (f"\n*** Zufällig Tasks in diesen Monat füllen")
    print (f"Monatsstart = {now}")
    print (f"+1Monat     = {mlater}\n")
    
    zufallz=now.replace(hour=9, minute=0, second=0)
    
    for d in range (1,35) :
        t=TiTra.Task.FindTaskName("sports")
        
        if None != t :
            cal.add(t.NewAction(zufallz))
            
            for z in range(0,5) :
                zufallz= zufallz + timedelta(weeks=0, days=0, hours=0, minutes=30+random.randrange(50), seconds=3)  
                t=TiTra.Task.FindTaskid(random.randrange(10)+1)
                cal.add(t.NewAction(zufallz))
    
            t=TiTra.Task.FindTaskName("End/Stop")
    
            if None != t :
                zufallz=zufallz.replace(hour=18)
                cal.add(t.NewAction(zufallz))
    
        zufallz=zufallz.replace(hour=9, minute=0, second=0)
        zufallz=zufallz + timedelta(days=1, hours=0, minutes=1, seconds=0)  
           
    

if False :  ### dont load the files

    with open('tasks.json', 'r') as f:
        all_tasks=TiTra.Task.ReadAllTasksFromJSON(f)
    with open('prj.json', 'r') as f:
        all_projects=TiTra.Project.ReadAllProjectsFromJSON(f)

    print ("\nAlle Projekte:\n")    
    pp.pprint(all_projects)
    print ("\nAlle Tasks:\n")    
    pp.pprint(all_tasks)
        
### dont load the files


print("generate tasks and projects")

p=TiTra.Project("NULL","0","#DDDDDD")
all_projects[p._name]=p

t=TiTra.Task("End/Stop","x","#DDDDDD")
all_task[t._name]=t
p.addTask(t)

p=TiTra.Project("Boooring Project","-","#8888FF")
all_projects[p._name]=p

t=TiTra.Task("Meetings","_","#8888FF")
all_task[t._name]=t
p.addTask(t)

t=TiTra.Task("Testing","_","#8888EE")
all_task[t._name]=t
p.addTask(t)

t=TiTra.Task("Coding","_","#7777DD")
all_task[t._name]=t
p.addTask(t)

t=TiTra.Task("documenting","~","#7777DD")
all_task[t._name]=t
p.addTask(t)


p=TiTra.Project("TiTraPy",")","#FF8888")
all_projects[p._name]=p

t=TiTra.Task("Testing","(","#8888EE")
all_task[t._name]=t
p.addTask(t)

t=TiTra.Task("Coding",")","#8888EE")
all_task[t._name]=t
p.addTask(t)

t=TiTra.Task("documenting","|","#8888EE")
all_task[t._name]=t
p.addTask(t)



p=TiTra.Project("private",".","#20FF20")
all_projects[p._name]=p


t=TiTra.Task("sports",":","#20FF20")
all_task[t._name]=t
p.addTask(t)

t=TiTra.Task("gaming",")","#20FF20")
all_task[t._name]=t
p.addTask(t)

t=TiTra.Task("shopping","|","#20FF20")
all_task[t._name]=t
p.addTask(t)


print("TiTra.Task.AllTasksStr()",TiTra.Task.AllTasksStr())


global g_cal
g_cal=TiTra.Calender()

testCal=TiTra.Calender()

print("\nLeerer Testcalender \n",testCal,"\n")

InitForTest(testCal)
print("\nGefüllter Testcalender \n",testCal,"\n")


'''
## Teste ...

### Task

* :white_check_mark: ✔️ StopAction(time)


### Calender

* :white_check_mark: ✔️ findExact
* :white_check_mark: ✔️ findBetween
* :white_check_mark: ✔️Calender.removeBetween

'''


#help(TiTra.Calender)

now=datetime.datetime.today()
now=now.replace(microsecond=0)

s=TiTra.Task.StopAction(now)

fro = now - timedelta(weeks=0, days=0, hours=0, minutes=1, seconds=1)  
til = now + timedelta(weeks=0, days=0, hours=0, minutes=1, seconds=1)  

print("\nremoveIDAtTime")
testCal.add(s)

print(f"\nStopAction hinzugefügt {s}")
pp.pprint(testCal)
assert 1 == testCal.removeIDAtTime(s._id,now), "Sollte einen Eintrag finden und löschen"
pp.pprint(testCal)


print("\nremoveBetween {fro} {til} =",testCal.removeBetween(fro,til))
testCal.add(s)

print(f"\nStopAction WIEDER hinzugefügt {s}")

found=testCal.findExact(now)
print(f"\nfindeExact = {now} == {found}\n ")
assert "stopper" == found._task._name , "Test auf < til : die Anzahl der Treffer sollte Länge 1 haben"







fro = now - timedelta(weeks=0, days=0, hours=0, minutes=1, seconds=1)  
til = now + timedelta(weeks=0, days=0, hours=0, minutes=1, seconds=1)  

found=testCal.findBetween(fro,til)
print(f"\nSuche testCal ab zwischen >= {fro} -  < {til}. len(found) = {found.len()} == 1?\n ")

assert 1 == found.len() , "Die Anzahl der Treffer sollte Länge 1 haben"

print(found)


fro = now
til = now + timedelta(weeks=0, days=0, hours=0, minutes=1, seconds=1)  

found=testCal.findBetween(fro,til)
print(f"\nSuche testCal ab zwischen >= {fro} -  < {til}. len(found) = {found.len()} == 1?\n ")
assert 1 == found.len() , "Test auf = fro : die Anzahl der Treffer sollte Länge 1 haben"

fro = now + timedelta(weeks=0, days=0, hours=0, minutes=0, seconds=1)  
til = now + timedelta(weeks=0, days=0, hours=0, minutes=1, seconds=1)  

found=testCal.findBetween(fro,til)
print(f"\nSuche testCal ab zwischen >= {fro} -  < {til}. len(found) = {found.len()} == 0?\n ")
assert 0 == found.len() , "Test auf > fro : die Anzahl der Treffer sollte Länge 0 haben"

fro = now - timedelta(weeks=0, days=0, hours=0, minutes=1, seconds=1)  
til = now 

found=testCal.findBetween(fro,til)
print(f"\nSuche testCal ab zwischen >= {fro} -  < {til}. len(found) = {found.len()} == 0?\n ")
assert 0 == found.len() , "Test auf < til : die Anzahl der Treffer sollte Länge 0 haben"


print("\n\nERFOLG *** \nStopAction und Calender.findBetween, Calender.findExact, Calender.removeBetween erfolgreich getestet\n\n")

'''
# Teste UI Funktionen

* :white_check_mark: ✔️ classmethod Task.UITasksList()
* :white_check_mark: ✔️ method Projet.UITasksList
* :white_check_mark: ✔️ method Calender.UIActionsOfDayList(self, day:datetime)
* :white_check_mark: ✔️ method Calender.UICalcDurations(self, day:datetime)
'''

print("Teste die UI Funktionen, die jeweils eine Liste von dict aller Einheiten zurückgeben, die Pytonista UI tauglich ist\n")

print("Task.UITasksList")
tl=TiTra.Task.UITasksList()
pp.pprint(tl)

# https://www.geeksforgeeks.org/ways-sort-list-dictionaries-values-python-using-lambda-function/
# sort a list of dict


t=TiTra.Task.FindTaskName("sports")
p=t._project

print("\n\nTasks von Standard vor Anfügen")
all_projects["Standard"].print_tasks()

print("\nStandard.UITasksList\n")
pp.pprint(p.UITasksList())

zufallz=datetime.datetime.now() - timedelta(weeks=0, days=0, hours=8)  
for z in range (0,10) :
    zufallz= zufallz - timedelta(weeks=0, days=0, hours=0, minutes=10+random.randrange(50), seconds=3)  
    t=TiTra.Task.FindTaskid(random.randrange(11))
    testCal.add(t.NewAction(zufallz))
    testCal.add(t.NewAction(zufallz- timedelta(weeks=0, days=2 )))


print("\nCalender UIActionsOfDayList\n")
now=datetime.datetime.today()
pp.pprint(testCal.UIActionsOfDayList(now))

print("\nCalender UICalcDurations\n")
pp.pprint(testCal.UICalcDurations())


'''
## Zufällig Actions zum globalen Kalender ergänzen
'''


zufallz=datetime.datetime.now() - timedelta(weeks=0, days=0, hours=8)  
for z in range (0,10) :
    zufallz= zufallz - timedelta(weeks=0, days=0, hours=0, minutes=10+random.randrange(50), seconds=3)  
    t=TiTra.Task.FindTaskid(random.randrange(11))
    testCal.add(t.NewAction(zufallz))
    testCal.add(t.NewAction(zufallz- timedelta(weeks=0, days=2 )))

print(testCal)    

if testCal.len() > 0 :
    print("\n>>> Calc Durations\n")
    erg=testCal.CalcDurations()
    pp.pprint(erg)
    
    import csv

    with open('testcal.minuten.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile,delimiter=";")
        # Durch dict iterieren und den Wert = Liste mit TaskName und Minuten in csv schreiben
        spamwriter.writerow(("Minuten","Aktivität","Projekt"))
        for k, v in erg.items():
            spamwriter.writerow(v)
    
else:
    print("\ntestCal Calender erst füllen, dann klappt es auch mit dem Auswerten!")