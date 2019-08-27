# TiTraPy
**Ti**me **Tra**cker in python for pythonista on IOS on iPad.

**The screen layout is right no to big for iPhones**

Main file is TiTraPy.py, which uses pythonista environment and libs in IOS


# In Developement

Code and Documentation are mixed in German and English, but mostly German!
Programms are useful and stable - so i believe and experience when i use them.

I started the first [stubble](doc.md) of user a manual and code documenation in [doc.md](doc.md)

# Files

## Main Application TiTraPy
* `TiTraPy.py` contains the user interface and the main application, only usable in pythonista environment
* `TiTraPy.pyui` contains the definition of the ui
* `DataSource.py` implements the data source classes for the table views
* `TiTra.py` contains classes for the "business logic" to manage tasks, actions and a calender. It can be tested and used in standard python environments.
* `tests.py` implements test routines for TiTra.py - not fully implemented yet
* `*.json` `*.csv` contain the data for tasks, projects and the calender

## Task & Project Editor
* `TasksProjects.py` implements a editor for tasks and project (files). Work in progress but already usefull and everthing necessary is working already.
* `Tasks.pyui` and `Projects.pyui`contain the ui definition


# urls to raw files in my github repository

Do they ever change? Don't think so

* [https://raw.githubusercontent.com/ArduFox/TiTraPy/master/TiTra.py](https://raw.githubusercontent.com/ArduFox/TiTraPy/master/TiTra.py)
* [https://raw.githubusercontent.com/ArduFox/TiTraPy/master/TiTraPy.py](https://raw.githubusercontent.com/ArduFox/TiTraPy/master/TiTraPy.py)
* [https://raw.githubusercontent.com/ArduFox/TiTraPy/master/TiTraPy.pyui](https://raw.githubusercontent.com/ArduFox/TiTraPy/master/TiTraPy.pyui)

# ToDo

* systematically complete test code for TiTra.py. rework test.py translate and give useful feedback about tests
* add fall back code, if opening / reading `*.json`or `*.csv` files fails and fill in some example entries at `today()`
* remove remaining debug `prints` and other code stubs used for developement from TyTraPy
* complete docstrings
* update and edit documentation. Add some screen shots.
* different layout for iPhone 
* :ok: Stubble of a tool to edit tasks and projects -> TasksProjects.py
* :ok: Make class Calender containing all Tasks, Projects and Actions
* New Name for class ShowTView >> TiTraPyGUI & :ok: rename pyui file
* :ok: Add Tool to download the 3 main files (Titra.py, TiTraPy.py, TiTraPy.pui, DataSources.py, TiTra.py,README.md) from this git 
* :ok: DataSources dont have access to global var g_cal for delete entries! New class variable in ShowTView!
* :ok: Implement [VersionInStatusBar](https://github.com/cvpe/Pythonista-scripts/blob/dfbf9c4ee8172138b4b64c760f89cea1ed5562df/VersionInStatusBar.py) into my own code
* :ok: collect and publish code for testing classes in TiTra.py from my Jupyter Notebook
* :ok: write a short but instructive user manual - even if it will bei soon outdated

# State and changes

## 24.07.2019 Version 00.76

Done some work on code and GUI

- console.hud used to show success at saving calender & hours.csv. 
- code reformatted PEP8 and cleaned
- fixed stupid error in TiTra.Calender.removeIDAtTime, when deleting very last item in Calender.
- Button Save is aware of information shown in panel / tableview and changes title and saves appropriate data
- using the new TiTra.Calender methods for reading and saving tasks, projects, calender
- at the end of the file, the Calender instance will be set to prefix DEV. All saved files will therfore start with DEV.
- enabling / disabling buttons and hiding labels depending whats to see in right / second tableview
- Using custom view for main view to trap will_change() for saving the calender just before app exits
- added controls for saving and sharing calculated hours per day/week/month
- added class variable myCalender in ShowTView, to contain the instance of TiTra.Calender

and there is now an additional application
* Working Stubble for editing tasks and projects = `TasksProjects.py`. Its already possible to change names and colors, to create new instances and to change the associated project of tasks

## 29.06.2019

* TiTra.py in den Basisklassen um Methoden zum Laden und Speichern der Tasks, Projects und Calender sowie Zeiten erweitert
* test.py erweitert und es läuft jetzt sinnvoll durch
    * noch zu viele Ausgaben / prints
    * Keine Vollständigkeit
    * tests eher wenig dokumentiert / erklärt
    * zu selten 
        * Ankündigung, was getestet wird
        * Ergebnisse durch asserts geprüft
        * positives Feedback, falls asserts fehlerfrei waren
* Rework GUI for APP 00.72
    * using now a segemented control to change view in second pane
    * remaining code of VersionInStatusbar eliminated
    * Using custom view for main view to trap will_change() for saving the calender just before app exits
    * cleaning up the ui
    * added controls for saving and mailing calculated hours per day/week/month
    * added non working stubble of code to realy save the hours
    


## 15 & 16.06.2019 ShowTView

* in `Action._init_` die Zeit auf Sekunden=0 und Mikrosekunden=0 geglättet
* Action neue Vergleichsfunktionen __eq__ __ne__ die vorher auf None testen 
* Views sehen jetzt richtig hübsch aus inkl **swipe delete** für Calender
* Neue Funktionen removeIDAtTime und UICalcDuration  -  läuft :+1:
* Speicherfunktionen [`get_available_memory(self):`](https://gist.github.com/lukaskollmer/a09c0278d2d224b9f4839a895ebb9988) von Lukas Kollmer in den Code integriert, sie schreiben sauber ins visuelle Log - es wird immer wieder Speicher freigegeben!

