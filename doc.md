# Documentation and user manual for **TiTraPy**

**Ti**me**Tra**cking**Py**thon Tool / Application for phytonista

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



# Documentation of Classes
