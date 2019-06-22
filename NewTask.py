# NewTask.py

import console, os, ui
import datetime
from datetime import timedelta
from datetime import date

import random
#import json
import re
#import csv
import os
import shutil

import TiTra

global g_cal
g_cal=TiTra.Calender()

console.clear()

# InitTaskProjects(False)
# DebugMiniAgenda(False)
# TiTra.ReadTasksProjects()

all_projects=dict()
all_task=dict()

with open('tasks.json', 'r') as f:
    all_tasks=TiTra.Task.ReadAllTasksFromJSON(f)
with open('prj.json', 'r') as f:
    all_projects=TiTra.Project.ReadAllProjectsFromJSON(f)


p=all_projects["Standard"]
print ("Standard Projekt\n",p,"\n")

new_t=TiTra.Task("BTFM","-")
new_t.SetProject(p)
print ("new_t {!s}".format(new_t))

new_t=TiTra.Task("Controlling","-")
new_t.SetProject(p)
print ("new_t {!s}".format(new_t))

console.set_color(0.8,0,0.2)

print("\nKopiere Originaldateien nach *.bak")
shutil.copy2("tasks.json" ,"tasks.json.bak")
shutil.copy2("prj.json" ,"prj.json.bak")

print("Speichere geänderte task.json und prj.json\n")
with open('tasks.json', 'w') as f:
    all_tasks=TiTra.Task.WriteAllTasksToJSON(f)
with open('prj.json', 'w') as f:
    all_projects=TiTra.Project.WriteAllProjectsToJSON(f)

console.set_color(0,0,0)
help("console.set_color")
