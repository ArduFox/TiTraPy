# Documentation and user manual for **TiTraPy**

**Ti**me**Tra**cking**Py**thon Tool / Application for phytonistas

# Goals

* Build a framework of classes to modell projects, tasks in that projects and finaly action, meaning time spent in that tasks. Those actions will be collected in a calender class
  * Calender should calculate hours spend in projects per day, week, month
* Build a UI in pythonista to work with those classes and show the results

# Usage

## editing and creating of tasks and projects

Right now, there is no GUI for that purpose.

In the to be published code to test the base classes will be examples how to manage tasks and projects by calling the class methods in python code. 
Its quite simple - i beliefe - but needs to be more usable via gui

## The App

### Reading Files 

At Startup three file will be read by the code:  

* `tasks.json` contains the definition of the tasks including to which project they belong
* `prj.json`contains the definition of projects including a list of tasks (by ID / Number)
* `cal.csv` contains the actions = tasks with given date and time

Actions only have a start date / time no duration or ending time. Each tasks ends, when the following tasks starts. Therefore a "Pause/End" tasks with ID==0 is necessary, that indicates idle times or end of (work)day.

### GUI

### Usage: Adding, deleting, viewing actions

At startup, the dattime picker shows the date and time right now. The left pane shows the actions of today and the right pane the selectable tasks.

Begin with selecting one tasks, then push the **Add** button and this will add a action with the selected task and start time from the datetime picker.

Delete actions by swipping left in the left pane.

Selecting other dates results in updating the panes with the appropriate data.

### Usage: Show work hours



# Documentation of Classes in TiTra.py  -> needs to be updated



# API

* [Class: Task](#class-task)
  * [Methods](#methods)
* [Class: Project](#class-project)
  * [Methods](#methods)
* [Class: Action](#class-action)
  * [Methods](#methods)
* [Class: Calender](#class-calender)
  * [Methods](#methods)
* [Functions](#functions)


## Class: Task

Beschreibt eine Tätigkeit bzw. Teilprojekt bzw. Aufgabe, die zu konkreten Zeiten getand werden kann bzw. auf die Zeiten gebucht werden können

## Methods


#### `SetProject(self,prj)`

  Projektnamen eintragen oder ändern.
  Hier wird geprüft, ob das Projekt sich ändert und in diesem
  Fall wird der Task aus dem anderen Projekt entfernt werden

#### `SetName(self,NewName) `

  Name des Tasks ändern

#### `NextID(cls)`
`@classmethod`

  Gibt die nächste ID-Nummer zurück, die für den nächsten Task vergeben wird

#### `FindTaskid(cls,id) `
`@classmethod`

  Finde den Task mit der <id>

#### `FindTaskName(cls,name) `
`@classmethod`

  Finde den ERSTEN Task mit dem <name>

#### `RemoveTaskid(cls,id) `
`@classmethod`

  Einen Task anhand seiner id entfernen und löschen

#### `AllTasksStr(cls)->str `
`@classmethod`

  Alle Tasks, die es gibt ausgeben
  return
      String mit allen Tasks

#### `UITasksList(cls) ->list`
`@classmethod`

  Alle Tasks, die es gibt als UI angenehme Liste ausgeben
  return
      list of dict of all tasks

#### `NewAction(self,time) `

  Neue Action mit definierter Zeit anlegen

#### `StartActionNow(self) `

  Neue Action jetzt anlegen

#### `StopAction(cls,time) `
`@classmethod`

  stopper Action mit definierter Zeit  anlegen um eine Aktivität zu beenden 
  return
    angelegte Action oder
    None, falls Task mit id=0 nicht gefunden wurde
    wäre 0 im Fehlerfall ein besserer Rückgabecode? TODO 

#### `attr_dict(self)`

  Kopiert und ändert das dict mit den Attributen der Klasse, so dass JSON damit klar kommt

#### `WriteAllTasksToJSON(cls,filehandle) -> str`
`@classmethod`

  Schreibt alle Tasks in eine Datei - Bereits doppeltes Schreiben in Dateien entfernt

#### `ReadAllTasksFromJSON(cls, filehandle) `
`@classmethod`

  Liest Tasks aus einer JSON Datei ein und legt diese an
  return
  Dictionary of new generated Tasks

#### `DeleteAllTasks(cls) `
`@classmethod`


#### `CopyDictAllTasks(cls) -> dict `
`@classmethod`

  Erstellt eine Kopie des internen Dictionarys über alle tasks
  return
      dict with all tasks
## Class: Project

Beschreibt ein Projekt, zu dem mehrere Taten gehören können

## Methods


#### `addTask(self,task)`

  Fügt einen Task zu einem Project hinzu, d.h. ein weiterer Eintrag im Dictionary. KEINE CHECKS

#### `removeTask(self,task)`

  Löscht einen Task aus einem Project KEINE CHECKS

#### `print_tasks(self)`

  Hübscher Ausdruck aller Tasks im Project

#### `UITasksList(self) ->list`

  UI freundliche Liste mit allen Tasks als String erstellen
  return
      list of dicts of strings of all tasks of this project

#### `find_task(self,key) `

  Fíndet eine Task des Projektes anhand seines Namens

#### `len(self) -> int`

  return Anzahl der Tasks im Project

#### `attr_dict(self)`

  Kopiert und ändert das self.__dict__ mit den Attributen der Klasse, so dass JSON damit klar kommt

#### `DeleteAllProjects(cls) `
`@classmethod`


#### `WriteAllProjectsToJSON(cls,filehandle) -> str`
`@classmethod`

  Schreibt alle Projects in eine Datei - Bereits doppeltes Schreiben in Dateien entfernt

#### `ReadAllProjectsFromJSON(cls, filehandle) `
`@classmethod`

  Liest Projekte aus einer JSON Datei ein und legt diese an
## Class: Action

Definiert eine Aktion mit einem Startdatum
VORSICHT: da __eq__ und __ne__ hier neu definiert sind und nur die Startzeit vergleichen
funktioniert z.B. der Vergleich None != Action nicht!

__eq__ __ne__ umgebaut und einen Test auf None vorgeschaltet

## Methods


#### `hms(self) -> str `

  return
## Class: Calender

Sammelt die Actions und verwaltet die Einträge und kann vermutlich auch zukünftig Berichte erstellen

## Methods


#### `append(self, act: Action) `

  Eine Action anfügen ohne Prüfung z.B. auf Doppelte Einträge bzw. Einträge mit zu geringem Abstand
  Neuer Name analog list.append wegen Konsistenz
  Kein Test ob act != None -> das geht nämlich nicht!

#### `add(self, act: Action) `

  TODO to be discontinued

#### `remove(self, act: Action) `

  Eine Action aus der Liste der Aktionen entfernen

#### `removeAtTime(self, time: datetime) `

  Die Action zu einer bestimmten Zeit aus der Liste der Aktionen entfernen

#### `removeIDAtTime(self, id_, time: datetime) `

  Finde genau die Action, mit genau der Uhrzeit und lösche sie
  return:
      die gefundene Action

#### `removeBetween(self, fro: datetime, til:datetime) -> int `

  Die Action zwischen zwei Zeitpunkten o <= action < o aus der Liste der Aktionen entfernen
  Benutzt findBetween
  return
      Anzahl der gelöschten Objekte

#### `len(self) -> int`

  return

#### `sort(self)`

  sortiere die Liste der Actions nach _start (=Zeit)

#### `findExact(self, time: datetime) `

  Finde den ersten Eintrag, die erste Action, mit genau der Uhrzeit / oder besser Zeitdifferenz <= 1 Sekunde?
  return:
      die gefundene Action

#### `findFuzzy(self, time: datetime, seconds_diff=10*60) `

  Sammle Actions mit ungefähr der Uhrzeit d.h. Abstand < Parameter seconds_diff 

#### `findBetween(self, start: datetime, end: datetime) `

  Sammle Actions mit self._start >= start und self._start < end

#### `findTask(self, search_task ) `

  Sammle Actions mit dieser Task, anhand Task._id

#### `CalcDurations(self) -> dict `

  Zeiten in einem kompletten Kalenderobject je Task sammeln, addieren und auf Minuten runden
  return
      Dictionary mit Task._id als Index und als Wert eine Liste Minuten, Task._name, Task._projektName

#### `UICalcDurations(self) -> list `

  Addding times for actions in this calender and
  build a list of dict, that fits the needs of the Pythonista UI

#### `MonthReport(self, date: datetime)  -> dict `

  Erstellt einen Monatsreport für den Monat, der in <date> angegeben wird
  Sollte ich an geeigneter Stelle auch den Monat integrieren in das dict?
  Ginge ja
  return
      dict with tasks and their monthly duration in minutes

#### `SaveAndRemoveMonth(self, date: datetime, path:str)  `

  Speichert die Actions für den Monat, der in <date> angegeben wird in einem CSV
  und löscht diese dann aus dem Calender >> NOCH NICHT IMPLEMENTIERT <<
  return
      ?

#### `listActionsOfToday(self) -> list `


#### `listActionsOfDay(self, day:datetime) -> list `


#### `UIActionsOfDayList(self, day:datetime) -> list `


#### `StartActionName(self,name,time) `

  Neue Action anhand Name in Calender einfügen

#### `StartActionNameTodayHM(self,name,hm) `

  Neue Action anhand Name in Calender für heute mit Uhrzeit HH:MM einfügen

#### `WriteCalToCSV(self,filehandle) -> int `

  Schreibt den Calender d.h. alle Action Einträge als csv Datei raus
  return
     Anzahl der geschriebenen Sätze

#### `ReadCalFromCSV(self,filehandle)`

  Liest einen Calender aus einem CSV d.h. alle Action Einträge werden neu angelegt
# Functions


#### `InitTaskProjects(deb)`


#### `ReadTasksProjects() `
