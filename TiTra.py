#!/usr/bin/python
#
# PyTiTra_Classes.py
#
# Implements classes with "bussiness logic" and data modell for Time Tracking
#
# No GUI Implementation and not depended on IOS pythonista. 
# Works and is tested in python and Jupyter Notebook
#
# fixed error when deleting last action in calender
# 
# - making sure there is always a task["0"] with ._id==0 and at least one project[...]
# - error handling in ReadCalFomCSV added to handle unknown task
# - problems when writing german umlauts solved by adding 
#   encoding='utf8',errors="ignore" to open file
#   Why is this only appearing in CSV and not on JSON?
#
# https://realpython.com/documenting-python-code/#why-documenting-your-code-is-so-important
#
# -------------------------------------------------------------------------------------
#    Licence & Copyright
# -------------------------------------------------------------------------------------
#
#    Copyright 2019 ArduFox (Wolfgang Fuchs)
#
#    This file is part of TiTraPy.
#
#    TiTraPy is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    TiTraPy is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with TiTraPy.  If not, see <http://www.gnu.org/licenses/>.
#

#import pprint

import datetime
from datetime import timedelta
from datetime import date

import os, shutil

#import random
import json
import re
import csv


class Task:
  '''Beschreibt eine Tätigkeit bzw. Teilprojekt bzw. Aufgabe, die zu konkreten 
    Zeiten getan werden kann bzw. auf die Zeiten gebucht werden können'''

  # Soll ich hier eine statische Liste aller tasks führen?
  # Dann könnte ich die hier lesen & finden
  # mindestens für Debugging

  __task_num = 0
  __all_tasks = dict()

  def __init__(self, name: str, emoij="X", farbe="#265B6A"):
    '''Neuen Task anlegen und im Dictionary aller tasks aufnehmen'''
    self._name = name
    self._emoij = emoij
    self._farbe = farbe
    self._projectName = ""
    self._project = None  # 0 oder none ??
    self._id = Task.__task_num
    Task.__task_num += 1
    self.__all_tasks[self._id] = self

  def __str__(self):
    return "Task ([%d]: %s, %s, %s, %s)" % (self._id, self._name, self._emoij,
                                            self._farbe, self._projectName)

  def SetProject(self, prj):
    """Projektnamen eintragen oder ändern.
          Hier wird geprüft, ob das Projekt sich ändert und in diesem
          Fall wird der Task aus dem anderen Projekt entfernt werden"""

    #        if self._project != 0 :

    if self._project != None:
      self._project.removeTask(self)

    self._projectName = prj._name
    self._project = prj
    self._project.addTask(self)

  def RemoveProject(self):
    self._projectName = ""
    self._project = None

  def UpdateProjectName(self, new_name: str):
    '''Update ONLY the projectName member'''
    self._projectName = new_name

  def SetName(self, NewName):
    '''Change name of task'''
    if self._project != None:
      # print("\n\n~~~~ PROBLEM Ändere Namen '{}' ~~~~\n".format(NewName))
      self._project.removeTask(self)  #  TODO not yet tested
      self._name = NewName
      self._project.addTask(self)
    else:
      self._name = NewName

  @classmethod
  def NextID(cls):
    'Gibt die nächste ID-Nummer zurück, die für den nächsten Task vergeben wird'
    return Task.__task_num

  @classmethod
  def FindTaskid(cls, id):
    '''find task with <id>
        return
          None if found nothing
        '''
        
    # https://realpython.com/python-keyerror/
    
    return cls.__all_tasks.get(id)

  @classmethod
  def FindTaskName(cls, name):
    '''find first task with <name>
        return
          None if found nothing'''

    for k, _t in cls.__all_tasks.items():
      if name == _t._name:
        return _t

    return None

  def RemoveTask(self):
    '''Remove Task by given id. 
           Remove it from associated Project
           What to do with associated actions?
        '''
    self._project.removeTask(self)
    self.__all_tasks.pop(self._id, None)

  @classmethod
  def AllTasksStr(cls) -> str:
    """Construct beautiful string of all tasks
            
        """

    s = "AllTasksStr:"
    for k, _t in cls.__all_tasks.items():
      s = s + f"\n{k}: {_t}"
    return s

  @classmethod
  def GetAllTasksList(cls) -> list:
    """Return the List of AllTasks __all_tasks
        """
    return cls.__all_tasks

  @classmethod
  def UITasksList(cls) -> list:
    """construct list of dicts of all tasks for usage in UI
        return
            list of dict of all tasks
        """

    l = list()
    for k, _t in cls.__all_tasks.items():
      l.append({
        "titl": f"{_t._name} '{_t._emoij}' [{_t._projectName}]",
        'id': f"{_t._id}",
        "task": _t._name,
        'prj': _t._projectName,
        'color': _t._farbe,
        'id': _t._id
      })
    l = sorted(l, key=lambda i: (i['prj'], i['task']))
    return l

  def NewAction(self, time):
    '''create new action with this task at given <time>
           return created action        '''
    act = Action(self, time)
    return act

  def StartActionNow(self):
    '''create new action with this task now
           return created action        '''
    act = Action(self, datetime.datetime.now())
    return act

  @classmethod
  def StopAction(cls, time):
    """create stopper action with id == 0 at given <time>
              return
                created action
                None, if task with id==0 dont exists"""

    _s = Task.FindTaskid(0)

    if None != _s:
      act = _s.NewAction(time)
      return act
    else:
      print("\nERROR\n     StopAction with _od==0 not found!\n")
      'Hier sollte ich eigentlich einen Fehler anzeigen'

    return None

  # return data representation for JSON object
  def attr_dict(self):
    'Kopiert und ändert das dict mit den Attributen der Klasse, so dass JSON damit klar kommt'

    # VORSICHT in python ist eine Zuweisung kein Kopieren eines Objectes in eine neue Instanz!
    odict = self.__dict__.copy()  # get attribute dictionary
    #        print(odict)
    del odict['_project']  # remove reference to project
    return odict

  @classmethod
  def WriteAllTasksToJSON(cls, filehandle) -> str:
    '''create JSON with all tasks
        return
           JSON String '''

    JSONstr = ""
    out_dict = dict()

    for _id, _t in cls.__all_tasks.items():

      out_dict[_t._id] = _t.attr_dict()
      # ok, so würden mehrere JSON Objekte in einem String / File landen aber das ist nicht decodierbar!
      # print (_t.attr_dict())
      # JSONstr = JSONstr + json.dumps({ _t._id : _t.attr_dict()})

      # jdict=json.loads(JSONstr)
      # print(jdict)

    json.dump(out_dict, filehandle, sort_keys=True, indent=2)

    JSONstr = json.dumps(out_dict, sort_keys=True, indent=2)
    # TestCode, der wieder einliest und nochmal schreibt, um die Ergebnisse vergleichen zu können

    # print(JSONstr)
    # jdict=json.loads(JSONstr)
    # JSONstr = json.dumps(jdict, sort_keys=True, indent=2)
    # print(JSONstr)
    #with open('tasks2.json', 'w') as f:
    #    json.dump(jdict, f, sort_keys=True, indent=2)

    # Es gibt einen Unterschied! In der originalen Datei wird der key numerisch sortiert und im Ergebnis alphanumerisch!
    # Muss also darauf achten, dass die _id nicht aus dem key sondern aus dem Attribut generiert wird
    return JSONstr

  @classmethod
  def ReadAllTasksFromJSON(cls, filehandle):
    """Read all tasks from JSON file and make sure, there is always a task["0"]
           return
           Dictionary of new generated Tasks"""

    jdict = dict()

    jdict = json.load(filehandle)

    # Eigentlich davor alle Tasks löschen!

    new_tasks = dict()
    max_id = 0
    nt = None

    for _id, _t in jdict.items():
      nt = Task(_t["_name"], _t["_emoij"], _t["_farbe"])
      nt._id = _t["_id"]
      new_tasks[_t["_id"]] = nt
      # print(f"{_t['_id']}: {nt}")
      max_id = max(nt._id, max_id)  # TODO 

    if None == new_tasks[0]:
      nt = Task("stop/pause", "X", "gray")
      nt._id = 0
      new_tasks[0] = nt

    if Task.NextID() <= max_id:
      print(f"\nReadAllTasksFromJSON: max_id={max_id} > .NextID() !! \n")
      Task.__task_num=max_id+1

    return new_tasks

  @classmethod
  def DeleteAllTasks(cls):
    for _id, _t in cls.__all_tasks.items():
      pass
    cls.__all_tasks.clear()
    cls.__task_num = 0

  @classmethod
  def CopyDictAllTasks(cls) -> dict:
    """ Deep copy __all_tasks into new dict
            return
                dict with all tasks
        """
    return cls.__all_tasks.copy()


class Project:
  'Beschreibt ein Projekt, zu dem mehrere Taten gehören können'

  __all_projects = dict()

  def __init__(self, name: str, emoij="X", farbe="#265B6A"):
    self._name = name
    self._emoij = emoij
    self._farbe = farbe
    self.__tasks = dict()
    self.__all_projects[name] = self

  # __tasks ist von aussen nicht sichtbar
  # _tasks wäre read only
  # alle anderen Atrribute können von außen zugegriffen werden

  def addTask(self, task):
    'Fügt einen Task zu einem Project hinzu, d.h. ein weiterer Eintrag im Dictionary. KEINE CHECKS'
    if None != task:
      self.__tasks[task._name] = task
      if task._project == None:
        task.SetProject(self)

  def removeTask(self, task):
    'Löscht einen Task aus einem Project KEINE CHECKS'
    'https://realpython.com/python-dicts/'

    # https://realpython.com/python-dicts/
    self.__tasks.pop(task._name, "")

  def RemoveProject(self):
    '''Remove this Project and remove it from all associated tasks
         
      '''
    for k, t in self.__tasks.items():
      t.RemoveProject()

    self.__all_projects.pop(self._name, "")

  def RenameProject(self, new_name):
    '''Rename this project and update all associated tasks
      '''
    #first remove from dict and then add with new name
    self.__all_projects.pop(self._name, "")
    self._name = new_name
    self.__all_projects[self._name] = self
    for k, t in self.__tasks.items():
      t.UpdateProjectName(new_name)

  def __str__(self):
    return "Project({}, {}, {} \n {} )".format(self._name, self._emoij,
                                               self._farbe, self.__tasks)

  def print_tasks(self):
    'Hübscher Ausdruck aller Tasks im Project'

    for k, t in self.__tasks.items():
      print(f"Task : {k} <{t._emoij}>  prj={t._projectName}")

  @classmethod
  def GetAllProjectsDict(cls) -> dict():
    '''returns the dict with all projects
      '''
    return cls.__all_projects

  @classmethod
  def GetAllProjectsList(cls) -> list():
    '''returns a sorted (by name) list of Project Objects -> they have no id!
      '''

    l = list()
    for k, _p in cls.__all_projects.items():
      l.append(_p)

    l = sorted(l, key=lambda i: (i._name))
    return l

  def UITasksList(self) -> list:
    """UI freundliche Liste mit allen Tasks als String erstellen
            return
                list of dicts of strings of all tasks of this project
        """

    l = list()
    for k, _t in self.__tasks.items():
      l.append({
        "titl": f"{_t._name} '{_t._emoij}' [{_t._projectName}]",
        'id': f"{_t._id}",
        "name": _t._name,
        'prj': _t._projectName,
        'color': _t._farbe,
        'id': _t._id
      })

    l = sorted(l, key=lambda i: (i['prj'], i['name']))
    return l

  @classmethod
  def UIProjectList(cls) -> list:
    erg_list = list()
    for _id, _p in cls.__all_projects.items():
      erg_list.append(_p._name)

    return erg_list

  def find_task(self, key):
    '''return the task with given keys in this project
    '''
    return self.__tasks[key]

  def len(self) -> int:
    '''return number of tasks in this project'''
    return len(self.__tasks)

  def attr_dict(self):
    '''Kopiert und ändert das self.__dict__ mit den Attributen der Klasse, so dass JSON damit klar kommt
        return
          modifizierte Kopie des self.__dict__'''

    # VORSICHT in python ist eine Zuweisung kein Kopieren eines Objectes in eine neue Instanz!
    odict = self.__dict__.copy()  # get attribute dictionary
    # print(odict)
    del odict["_Project__tasks"]  # remove reference to project

    l = list()
    for k, _t in self.__tasks.items():
      l.append(_t._id)

    odict["tasks"] = l
    # print (odict)
    return odict

  def DeleteAllProjects(cls):

    cls.__all_projects.clear()
    cls.__task_num = 0

  @classmethod
  def WriteAllProjectsToJSON(cls, filehandle) -> str:
    '''Schreibt alle Projects in eine Datei - Bereits doppeltes Schreiben in Dateien entfernt
        return
           JSON String In der aktuellen Arbeitsversion '''

    JSONstr = ""
    out_dict = dict()

    for _id, _p in cls.__all_projects.items():
      out_dict[_p._name] = _p.attr_dict()

    json.dump(out_dict, filehandle, sort_keys=True, indent=2)

    # TestCode, der wieder einliest und nochmal schreibt, um die Ergebnisse vergleichen zu können
    # jdict=json.loads(JSONstr)
    # with open('prj2.json', 'w') as f:
    #     json.dump(jdict, f, sort_keys=True, indent=2)

    JSONstr = json.dumps(out_dict, sort_keys=True, indent=2)
    return JSONstr

  @classmethod
  def ReadAllProjectsFromJSON(cls, filehandle):
    '''Read projects from JSON file
        return
          Dictionary mit den neuen Projekten'''

    jdict = dict()

    jdict = json.load(filehandle)

    new_prj = dict()

    for _id, _p in jdict.items():
      np = Project(_p["_name"], _p["_emoij"], _p["_farbe"])
      new_prj[_p["_name"]] = np
      # print(f"{_p['_name']}: {np}")

      for tid in _p["tasks"]:
        _t = Task.FindTaskid(tid)
        # print(f"{tid} = {_t._name}")
        _t.SetProject(np)

    
    # check if there is at least one project 
    
    if len(new_prj) == 0 :
      np = Project("default", ".", "grey")
      new_prj["default"] = np      
    
    return new_prj


class Action:
  def __init__(self, task: Task, zeit=datetime.datetime.now()):
    'Neue Action erzeugen und in datetime seconds und microseconds auf 0 setzen'
    self._start = zeit.replace(second=0, microsecond=0)
    self._task = task
    self._id = task._id

  # https://docs.python.org/3.7/library/string.html#formatstrings
  # strftime("%m/%d/%Y, %H:%M:%S")

  def hms(self) -> str:
    'return'
    '  Uhrzeit der Action in der Form HH:MM:SS'
    return self._start.strftime("%H:%M:%S")

  def __str__(self):
    return "Action({} : {})".format(
      self._start.strftime("%Y-%m-%d %H:%M:%S"), self._task._name)

  # https://docs.python.org/3.3/reference/datamodel.html?highlight=__lt__#object.__lt__
  def __lt__(self, other):
    return self._start < other._start

  def __le__(self, other):
    return self._start <= other._start

  def __gt__(self, other):
    return self._start > other._start

  def __ge__(self, other):
    return self._start >= other._start

  def __eq__(self, other):
    if other == None:
      return False
    else:
      return self._start == other._start

  def __ne__(self, other):
    if other == None:
      return True
    else:
      return self._start != other._start

  # https://docs.python.org/3/library/datetime.html
  def __sub__(self, other):
    '''difference in starttime of two actions in seconds'''

    td = (self._start - other._start)
    #        return td.seconds  # So funktioniert das nicht, weil keine negative Zahlen entstehen und maximale Differenz ein Tag ist 
    return int(td.total_seconds())


class Calender:
  '''Sammelt die Actions und verwaltet die Einträge und kann vermutlich auch zukünftig Berichte erstellen'''

  def __init__(self, prefix="tt"):
    '''
        Init the calender

        attributes:
            private: 
                __acttions_list
                __notsorted
                __prefix
                __dirty
        '''
    self.__actions = list()
    self.__notsorted = False
    self.__prefix = prefix
    self.__dirty = False

  def GetPrefix(self) -> str:
    return self.__prefix

  def append(self, act: Action):
    """Eine Action anfügen ohne Prüfung z.B. auf Doppelte Einträge bzw. Einträge mit zu geringem Abstand
           Neuer Name analog list.append wegen Konsistenz
           Kein Test ob act != None -> das geht nämlich nicht!"""
    self.__actions.append(act)
    self.__notsorted = True
    self.__dirty = True

  def add(self, act: Action):
    """TODO to be discontinued"""
    self.append(act)

  def remove(self, act: Action):
    'Eine Action aus der Liste der Aktionen entfernen'

    self.__actions.remove(act)
    self.__dirty = True

  def removeAtTime(self, time: datetime):
    'Die Action zu einer bestimmten Zeit aus der Liste der Aktionen entfernen'
    act = self.findExact(time)
    self.__actions.remove(act)
    self.__dirty = True

  def removeIDAtTime(self, id_, time: datetime) -> Task:
    ''' delete the action with given id and time
         return:
             found action
             None if nothing found'''

    time = time.replace(second=0, microsecond=0)

    if self.__notsorted:
      self.sort()

    for i in range(len(self.__actions) - 1, 0, -1):
      if self.__actions[i]._start < time:
        break
      if self.__actions[i]._start == time:
        if self.__actions[i]._id == id_:
          a = self.__actions[i]
          self.__actions.remove(self.__actions[i])
          self.__dirty = True
          return a
    'Wenn die Schleife komplett durchläuft dann wurde nichts gefunden'

    return None

  def removeBetween(self, fro: datetime, til: datetime) -> int:
    """Die Action zwischen zwei Zeitpunkten o <= action < o aus der Liste der Aktionen entfernen
            Benutzt findBetween
            return
                Anzahl der gelöschten Objekte"""

    fcal = self.findBetween(fro, til)
    i = 0
    for _a in fcal.__actions:
      self.__actions.remove(_a)
      self.__dirty = True
      i = i + 1

    return i

  def __str__(self):
    s = "Calender(\n"
    for a in self.__actions:
      s += "  {0}\n".format(a)
    return s + ")"

  def len(self) -> int:
    'return'
    '  Anzahl der Actions im Calender'
    return len(self.__actions)

  def sort(self):
    'sortiere die Liste der Actions nach _start (=Zeit)'

    self.__actions.sort()
    self.__notsorted = False

  def findExact(self, time: datetime):
    ''' Finde den ersten Eintrag, die erste Action, mit genau der Uhrzeit / oder besser Zeitdifferenz <= 1 Sekunde?
         return:
             die gefundene Action'''

    if self.__notsorted:
      self.sort()
    for id in range(len(self.__actions) - 1, 0, -1):
      if self.__actions[id]._start < time:
        break
      if self.__actions[id]._start == time:
        return self.__actions[id]
    #Wenn die Schleife komplett durchläuft dann wurde nichts gefunden
    return None  # TODO wäre RÜckgabe von 0 im Fehlerfall besser? 

  def findFuzzy(self, time: datetime, seconds_diff=10 * 60):
    '''collect action around given time 
         return:
             Neues Calender Objekt mit den gefundenen Actions, reverse order'''
    td = timedelta(weeks=0, days=0, hours=0, minutes=0, seconds=seconds_diff)

    print("** FindeFuzzy {} {}={}".format(time, seconds_diff, td))
    print("** {} bis {}".format(time - td, time + td))
    # print ("** ",list(range(len(self.__actions)-1,0,-1)),"\n")

    if self.__notsorted:
      self.sort()

    foundCal = Calender()

    for id in range(len(self.__actions) - 1, 0, -1):
      # print ("   {}= {} diff = {}".format(id,self.__actions[id],self.__actions[id]._start-time))
      if self.__actions[id]._start < (time - td):
        break
      if self.__actions[id]._start < (time + td):
        foundCal.add(self.__actions[id])

    return foundCal

  def findBetween(self, start: datetime, end: datetime):
    '''collect actions with self._start >= start und self._start < end
         return:
             new calender object with only found actions, NON reverse order'''

    if self.__notsorted:
      self.sort()

    foundCal = Calender()

    for id in range(len(self.__actions) - 1, 0, -1):
      # print ("   {}= {} diff = {}".format(id,self.__actions[id],self.__actions[id]._start-start))
      if self.__actions[id]._start < start:
        break
      if self.__actions[id]._start < end:
        foundCal.add(self.__actions[id])

    foundCal.sort()
    return foundCal

  def findTask(self, search_task):
    '''collect all actions with given Task._id <search_task>
         return:
             new calender object with only found actions, NON reverse order'''

    # print ("** findTask {} ".format(search_task._name))

    if self.__notsorted:
      self.sort()

    foundCal = Calender()

    for id in range(0, len(self.__actions) - 1):
      if self.__actions[id]._id == search_task._id:
        foundCal.add(self.__actions[id])

    foundCal.sort()
    return foundCal

  def CalcDurations(self) -> dict:
    """ Zeiten in einem kompletten Kalenderobject je Task sammeln, addieren und auf Minuten runden
            return
                Dictionary mit Task._id als Index und als Wert eine Liste Minuten, Task._name, Task._projektName
        """

    if self.__notsorted:
      self.sort()

    minu = dict()

    l = len(self.__actions)
    for index in range(0, len(self.__actions) - 1):
      _a = self.__actions[index]
      td = self.__actions[index + 1]._start - _a._start
      # print(f"*** {index} von {l} : {self.__actions[index]._task._name} = {td} = {round(td.total_seconds()/60)}")

      if _a._id in minu:
        # print(f"{index}: aufaddieren {minu[_a._id]} t={minu[_a._id][0]}")
        t = minu[_a._id][0] + round(td.total_seconds() / 60)
        h = round(t / 60 * 10) / 10
        minu[_a._id] = (t, h, _a._task._name, _a._task._projectName)

      else:
        t = round(td.total_seconds() / 60)
        minu[_a._id] = (t, round(t / 60 * 10) / 10, _a._task._name,
                        _a._task._projectName)
        # print(f"{index}: neu erzeugt: {minu[_a._id]}")
    if 0 in minu:
      del minu[0]
    return minu

  def WriteDurationsToCSV(self, filehandle):
    '''Call CalcDuration and write csv to <filehandle>
    '''

    erg = self.CalcDurations()

    # how can i sort this dict with values, that are lists?        

    spamwriter = csv.writer(filehandle, delimiter=";")
    # Durch dict iterieren und den Wert = Liste mit TaskName und Minuten in csv schreiben
    spamwriter.writerow(("Minutes", "Hours", "Task", "Project"))
    for k, v in erg.items():
      spamwriter.writerow(v)


  def UICalcDurations(self) -> list:
    """Addding times for actions in this calender and
        build a list of dict, that fits the needs of the Pythonista UI
        """

    dl = self.CalcDurations()

    l = list()
    for k, v in dl.items():
      if k != "Date" and k != "0" and k != 0:
        l.append({
          "title": f"{v[2]}",
          'hour': round(v[0] / 6) / 10,
          'prj': f"{v[3]}"
        })

#        l =sorted(l, key = lambda i: (i['prj']))

# negative Stundenzahl als Sortierkriterium
    l = sorted(l, key=lambda i: (i['prj'], -i['hour']))
    #       l= sorted(l, key = lambda i: (i['prj'], i['name'])) 

    # https://www.geeksforgeeks.org/ways-sort-list-dictionaries-values-python-using-itemgetter/
    return l

  def MonthReport(self, date: datetime) -> dict:
    """ Create monthly report in month of <date> 
            return
                dict with tasks and their monthly duration in minutes
        """
            
    mstart = date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    mend = mstart + timedelta(weeks=0, days=32, hours=0, minutes=0, seconds=0)
    mend = mend.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    mcal = self.findBetween(mstart, mend)
    d = mcal.CalcDurations()

    d["Date"] = (date, mstart, mend)
    return d

  def SaveAndRemoveMonth(self, date: datetime, path: str):
    """ save actions in month of <date>  in own CSV at given <path>
        and remove them from calender
        
        useful for cleanup of to large calenders
            return
                ?
        """
    mstart = date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    mend = mstart + timedelta(weeks=0, days=32, hours=0, minutes=0, seconds=0)
    mend = mend.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    print(f"\n\*** SaveAndRemoveMonth({date} to {path})")
    print(f"    Monatsstart = {mstart}")
    # print(f"    +1Monat     = {mend}")

    mcal = self.findBetween(mstart, mend)

    fname = path + mstart.strftime("%Y_%m") + "_TiTraCal.csv"
    print(f"    Filename = {fname}")

    with open(fname, 'w', newline='') as f:
      w = mcal.WriteCalToCSV(f)

    print(f"    written = {w}")

    self.removeBetween(
      mstart, mend
    )  # TODO kontrollieren, ob diese Routine auch die selben Regeln auswertet wie find ...
    return w

  def listActionsOfToday(self) -> list:
    now = datetime.datetime.now()
    return self.listActionsOfDay(now)

  def listActionsOfDay(self, day: datetime) -> list:

    dstart = day.replace(hour=0, minute=0, second=0, microsecond=0)
    dend = dstart + timedelta(days=1)

    dcal = self.findBetween(dstart, dend)

    dlist = list()
    for a in dcal.__actions:
      td = (a._start - dstart)
      mi = round(td.total_seconds() / 60)
      dlist.append(
        (mi, a._task._farbe, a._start.strftime("%H:%M"), a._task._name,
         a._task._projectName, a._start.strftime("%Y-%m-%d")))

    return dlist

  def UIActionsOfDayList(self, day: datetime) -> list:
    '''create list of actions at given day in UI friendly format
           return
              created list'''
    dstart = day.replace(hour=0, minute=0, second=0, microsecond=0)
    dend = dstart + timedelta(days=1)

    dcal = self.findBetween(dstart, dend)

    dlist = list()
    for a in dcal.__actions:
      td = (a._start - dstart)
      mi = round(td.total_seconds() / 60)
      d = {
        'long':
        f"{a._start.strftime('%H:%M')} {a._task._name} [{a._task._projectName}]",
        'task':
        a._task._name,
        'prj':
        a._task._projectName,
        'id':
        a._task._id,
        'color':
        a._task._farbe,
        'minute':
        mi,
        'time':
        a._start.strftime('%H:%M'),
        'date':
        a._start.strftime('%Y-%m-%d')
      }

      # print(d)
      dlist.append(d)

    return dlist

  def StartActionName(self, name, time):
    '''create new action with given task <name> at given <time>'
        return
          new action'''
          
    _t = Task.FindTaskName(name)

    if None != _t:
      _a = _t.NewAction(time)
      self.add(_a)
      return (_a)

    return (None)

  def StartActionNameTodayHM(self, name, hm):
    '''create new action with given task <name> today at given hh:mm'
        return
          new action'''

    _t = Task.FindTaskName(name)

    if None != _t:
      time = datetime.datetime.now()
      regex = r"([0-2]?\d):([0-6]\d)"

      m = re.match(regex, hm)

      if m:
        # print (m.groups())
        # print (m.group(0))
        # print (m.group(1))
        # print (m.group(2))

        time = time.replace(
          hour=int(m.group(1)),
          minute=int(m.group(2)),
          second=0,
          microsecond=0)
        _a = _t.NewAction(time)
        self.add(_a)
        return (_a)
    return (None)

  def SaveCal(self) -> int:
    '''Save the Calender Data to CSV
            filename <prefix>.cal.csv

            check if __dirty
            check if file exists, then copy to *bak.csv
        '''

    if self.__dirty:
      if os.path.exists(self.__prefix + ".cal.csv"):
        shutil.copy2(self.__prefix + ".cal.csv",
                     self.__prefix + ".cal.bak.csv")
      with open(self.__prefix + ".cal.csv", "w",encoding='utf8',errors="ignore") as f:
        i = self.WriteCalToCSV(f)
        self.__dirty = False
        return i

  def WriteCalToCSV(self, filehandle) -> int:
    """write calender with all actions into given <filehandle> as csv
            return
               number of written actions"""
               
    if self.__notsorted:
      self.sort()

    writer = csv.writer(
      filehandle, delimiter=";", quoting=csv.QUOTE_NONNUMERIC)
    writer.writerow(("Zeit", "Name", "Projekt", "ID"))

    written = 0

    #        for index in range(0,len(self.__actions)-1) :
    #            _a=self.__actions[index]
    
    # TODO SaveCalender cant write german umlauts "äöüÄÖÜß" !!! Maybe this a problem of file open!
    
    for _a in self.__actions:
      writer.writerow((_a._start, _a._task._name, _a._task._projectName,
                       _a._task._id))
      written += 1

    return written

  def LoadCal(self):
    with open(self.__prefix + ".cal.csv", "r",encoding='utf8',errors="ignore") as f:
      self.ReadCalFromCSV(f)

  def ReadCalFromCSV(self, filehandle):
    '''Read calender - all actions - out of csv file with given <filehandle>
       and build up all necessary objects into this calender
       
       what happens if in action referenced task cant be found? ignored!
    '''
    
    # https://realpython.com/python-csv/
    # https://docs.python.org/3/library/csv.html

    reader = csv.DictReader(
      filehandle, delimiter=";", quoting=csv.QUOTE_NONNUMERIC)
    try:
      for row in reader:
        # print(row)
        _t = Task.FindTaskid(int(row['ID']))
        dt = datetime.datetime.strptime(row['Zeit'], "%Y-%m-%d %H:%M:%S")
        
        if None != _t :
          _a = _t.NewAction(dt)
          self.add(_a)
        else :
          print (f"** ERROR in TiTra.ReadCalFromCSV: action with taskid {row['ID']} at {row['Zeit']} unknown and NOT created")
          
          
    except csv.Error as e:
      print('file {}, line {}: {}'.format(filehandle, reader.line_num, e))
      exit(1)

  def SaveTasks(self) -> int:
    '''Save the tasks data to json
            filename <prefix>.tasks.json

            check if file exists, then copy to *bak.json
        '''

    if True:
      if os.path.exists(self.__prefix + ".tasks.json"):
        shutil.copy2(self.__prefix + ".tasks.json",
                     self.__prefix + ".tasks.bak.json")
      with open(self.__prefix + ".tasks.json", "w") as f:
        return len(Task.WriteAllTasksToJSON(f))

  def LoadTasks(self) -> int:
    '''Load the tasks data from json
            filename <prefix>.tasks.json
        '''
        
    # TODO test what happens, when a non existing file should be read!
    with open(self.__prefix + ".tasks.json", 'r') as f:
      at = Task.ReadAllTasksFromJSON(f)
      return len(at)

  def SaveProjects(self) -> int:
    '''Save the tasks data to json
            filename <prefix>.prj.json

            check if file exists, then copy to *bak.csv
        '''

    if True:
      if os.path.exists(self.__prefix + ".prj.json"):
        shutil.copy2(self.__prefix + ".prj.json",
                     self.__prefix + ".prj.bak.json")
      with open(self.__prefix + ".prj.json", "w") as f:
        return len(Project.WriteAllProjectsToJSON(f))

  def LoadProjects(self) -> int:
    '''Load the projects data from json
            filename <prefix>.tasks.json
        '''
    with open(self.__prefix + ".prj.json", 'r') as f:
      ap = Project.ReadAllProjectsFromJSON(f)
      return len(ap)



def ReadTasksProjects():
  with open('tasks.json', 'r') as f:
    Task.ReadAllTasksFromJSON(f)
  with open('prj.json', 'r') as f:
    Project.ReadAllProjectsFromJSON(f)

