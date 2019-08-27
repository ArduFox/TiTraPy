# TiTra



# API

* [Class: Task](#class-task)
  * [Methods](#methods)
* [Class: Project](#class-project)
  * [Methods](#methods)
* [Class: Action](#class-action)
  * [Methods](#methods)
* [Class: Calender](#class-calender)
  * [Methods](#methods)


## Class: Task

Beschreibt eine Tätigkeit bzw. Teilprojekt bzw. Aufgabe, die zu konkreten 
Zeiten getan werden kann bzw. auf die Zeiten gebucht werden können

## Methods


#### `SetProject(self, prj)`

  Projektnamen eintragen oder ändern.
  Hier wird geprüft, ob das Projekt sich ändert und in diesem
  Fall wird der Task aus dem anderen Projekt entfernt werden

#### `RemoveProject(self)`


#### `UpdateProjectName(self, new_name: str)`

  Update ONLY the projectName member

#### `SetName(self, NewName)`

  Change name of task

#### `NextID(cls)`
`@classmethod`

  Gibt die nächste ID-Nummer zurück, die für den nächsten Task vergeben wird

#### `FindTaskid(cls, id)`
`@classmethod`

  find task with <id>
  return
    None if found nothing

#### `FindTaskName(cls, name)`
`@classmethod`

  find first task with <name>
  return
    None if found nothing

#### `RemoveTask(self)`

  Remove Task by given id. 
  Remove it from associated Project
  What to do with associated actions?

#### `AllTasksStr(cls) -> str`
`@classmethod`

  Construct beautiful string of all tasks
              
          

#### `GetAllTasksList(cls) -> list`
`@classmethod`

  Return the List of AllTasks __all_tasks
          

#### `UITasksList(cls) -> list`
`@classmethod`

  construct list of dicts of all tasks for usage in UI
  return
      list of dict of all tasks

#### `NewAction(self, time)`

  create new action with this task at given <time>
  return created action        

#### `StartActionNow(self)`

  create new action with this task now
  return created action        

#### `StopAction(cls, time)`
`@classmethod`

  create stopper action with id == 0 at given <time>
  return
    created action
    None, if task with id==0 dont exists

#### `attr_dict(self)`

  Kopiert und ändert das dict mit den Attributen der Klasse, so dass JSON damit klar kommt

#### `WriteAllTasksToJSON(cls, filehandle) -> str`
`@classmethod`

  create JSON with all tasks
  return
     JSON String 

#### `ReadAllTasksFromJSON(cls, filehandle)`
`@classmethod`

  Read all tasks from JSON file and make sure, there is always a task["0"]
  return
  Dictionary of new generated Tasks

#### `DeleteAllTasks(cls)`
`@classmethod`


#### `CopyDictAllTasks(cls) -> dict`
`@classmethod`

  Deep copy __all_tasks into new dict
  return
      dict with all tasks
## Class: Project

Beschreibt ein Projekt, zu dem mehrere Taten gehören können

## Methods


#### `addTask(self, task)`

  Fügt einen Task zu einem Project hinzu, d.h. ein weiterer Eintrag im Dictionary. KEINE CHECKS

#### `removeTask(self, task)`

  Löscht einen Task aus einem Project KEINE CHECKS

#### `RemoveProject(self)`

  Remove this Project and remove it from all associated tasks
           
        

#### `RenameProject(self, new_name)`

  Rename this project and update all associated tasks
        

#### `print_tasks(self)`

  Hübscher Ausdruck aller Tasks im Project

#### `GetAllProjectsDict(cls) -> dict()`
`@classmethod`

  returns the dict with all projects
        

#### `GetAllProjectsList(cls) -> list()`
`@classmethod`

  returns a sorted (by name) list of Project Objects -> they have no id!
        

#### `UITasksList(self) -> list`

  UI freundliche Liste mit allen Tasks als String erstellen
  return
      list of dicts of strings of all tasks of this project

#### `UIProjectList(cls) -> list`
`@classmethod`


#### `find_task(self, key)`

  return the task with given keys in this project
      

#### `len(self) -> int`

  return number of tasks in this project

#### `attr_dict(self)`

  Kopiert und ändert das self.__dict__ mit den Attributen der Klasse, so dass JSON damit klar kommt
  return
    modifizierte Kopie des self.__dict__

#### `DeleteAllProjects(cls)`


#### `WriteAllProjectsToJSON(cls, filehandle) -> str`
`@classmethod`

  Schreibt alle Projects in eine Datei - Bereits doppeltes Schreiben in Dateien entfernt
  return
     JSON String In der aktuellen Arbeitsversion 

#### `ReadAllProjectsFromJSON(cls, filehandle)`
`@classmethod`

  Read projects from JSON file
  return
    Dictionary mit den neuen Projekten
## Class: Action

## Methods


#### `hms(self) -> str`

  return
## Class: Calender

Sammelt die Actions und verwaltet die Einträge und kann vermutlich auch zukünftig Berichte erstellen

## Methods


#### `GetPrefix(self) -> str`


#### `append(self, act: Action)`

  Eine Action anfügen ohne Prüfung z.B. auf Doppelte Einträge bzw. Einträge mit zu geringem Abstand
  Neuer Name analog list.append wegen Konsistenz
  Kein Test ob act != None -> das geht nämlich nicht!

#### `add(self, act: Action)`

  TODO to be discontinued

#### `remove(self, act: Action)`

  Eine Action aus der Liste der Aktionen entfernen

#### `removeAtTime(self, time: datetime)`

  Die Action zu einer bestimmten Zeit aus der Liste der Aktionen entfernen

#### `removeIDAtTime(self, id_, time: datetime) -> Task`

  delete the action with given id and time
  return:
      found action
      None if nothing found

#### `removeBetween(self, fro: datetime, til: datetime) -> int`

  Die Action zwischen zwei Zeitpunkten o <= action < o aus der Liste der Aktionen entfernen
  Benutzt findBetween
  return
      Anzahl der gelöschten Objekte

#### `len(self) -> int`

  return

#### `sort(self)`

  sortiere die Liste der Actions nach _start (=Zeit)

#### `findExact(self, time: datetime)`

  Finde den ersten Eintrag, die erste Action, mit genau der Uhrzeit / oder besser Zeitdifferenz <= 1 Sekunde?
  return:
      die gefundene Action

#### `findFuzzy(self, time: datetime, seconds_diff=10 * 60)`

  collect action around given time 
  return:
      Neues Calender Objekt mit den gefundenen Actions, reverse order

#### `findBetween(self, start: datetime, end: datetime)`

  collect actions with self._start >= start und self._start < end
  return:
      new calender object with only found actions, NON reverse order

#### `findTask(self, search_task)`

  collect all actions with given Task._id <search_task>
  return:
      new calender object with only found actions, NON reverse order

#### `CalcDurations(self) -> dict`

  Zeiten in einem kompletten Kalenderobject je Task sammeln, addieren und auf Minuten runden
  return
      Dictionary mit Task._id als Index und als Wert eine Liste Minuten, Task._name, Task._projektName

#### `WriteDurationsToCSV(self, filehandle)`

  Call CalcDuration and write csv to <filehandle>
      

#### `UICalcDurations(self) -> list`

  Addding times for actions in this calender and
  build a list of dict, that fits the needs of the Pythonista UI

#### `MonthReport(self, date: datetime) -> dict`

  Create monthly report in month of <date> 
  return
      dict with tasks and their monthly duration in minutes

#### `SaveAndRemoveMonth(self, date: datetime, path: str)`

  save actions in month of <date>  in own CSV at given <path>
  and remove them from calender
  
  useful for cleanup of to large calenders
      return
          ?

#### `listActionsOfToday(self) -> list`


#### `listActionsOfDay(self, day: datetime) -> list`


#### `UIActionsOfDayList(self, day: datetime) -> list`

  create list of actions at given day in UI friendly format
  return
     created list

#### `StartActionName(self, name, time)`

  create new action with given task <name> at given <time>'
  return
    new action

#### `StartActionNameTodayHM(self, name, hm)`

  create new action with given task <name> today at given hh:mm'
  return
    new action

#### `SaveCal(self) -> int`

  Save the Calender Data to CSV
  filename <prefix>.cal.csv
  
  check if __dirty
  check if file exists, then copy to *bak.csv

#### `WriteCalToCSV(self, filehandle) -> int`

  write calender with all actions into given <filehandle> as csv
  return
     number of written actions

#### `LoadCal(self)`


#### `ReadCalFromCSV(self, filehandle)`

  Read calender - all actions - out of csv file with given <filehandle>
  and build up all necessary objects into this calender
  
  what happens if in action referenced task cant be found? ignored!

#### `SaveTasks(self) -> int`

  Save the tasks data to json
  filename <prefix>.tasks.json
  
  check if file exists, then copy to *bak.json

#### `LoadTasks(self) -> int`

  Load the tasks data from json
  filename <prefix>.tasks.json

#### `SaveProjects(self) -> int`

  Save the tasks data to json
  filename <prefix>.prj.json
  
  check if file exists, then copy to *bak.csv

#### `LoadProjects(self) -> int`

  Load the projects data from json
  filename <prefix>.tasks.json

#### `ReadTasksProjects()`

