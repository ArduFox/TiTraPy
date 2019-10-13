# TiTraPy



# API

* [Class: MyView](#class-myview)
  * [Methods](#methods)
* [Class: BoxPlotView](#class-boxplotview)
  * [Methods](#methods)
* [Class: ShowTableView](#class-showtableview)
  * [Methods](#methods)


## Class: MyView

from pythonista ui documentation
I need it to implement will_close() to save the data when ui is exited

Lessons learned
- View is the only ui class that can be subclassed - tells the doc
- How can I load a pyui file in my own class
  In the GUI Editor use the field Custom View Class at the bottom
  
- See https://forum.omz-software.com/topic/989/any-ui-module-tutorials-out-there/29
- there are best practice rules in that thread
- and a tutorial  

## Methods


#### `setCalender(self, cal: TiTra.Calender)`


#### `did_load(self)`


#### `will_close(self)`


#### `draw(self)`


#### `layout(self)`


#### `touch_began(self, touch)`


#### `touch_moved(self, touch)`


#### `touch_ended(self, touch)`


#### `keyboard_frame_will_change(self, frame)`


#### `keyboard_frame_did_change(self, frame)`

## Class: BoxPlotView

## Methods


#### `did_load(self)`


#### `will_close(self)`


#### `SetActions(self,acts:list)`


#### `draw(self)`


#### `keyboard_frame_will_change(self, frame)`


#### `keyboard_frame_did_change(self, frame)`

## Class: ShowTableView

## Methods


#### `LogMessage(self, line: str)`

  log a message to MessageBoard to show the user / developer what happend
          

#### `bt_empty_action(self, sender)`

  clear tableview1
          

#### `bt_task_action(self, sender)`

  fill "tableview1" with List of Tasks
          

#### `bt_cal2_action(self, sender)`

  fill "tableview2" with list of calender entries = actions
          

#### `bt_dur_day_action(self, sender)`

  fill "tableview1" with list of duration of tasks in selcted day
  Anzeigen welche Zeiten für welche Tasks gebraucht wurden

#### `bt_dur_week_action(self, sender)`

  fill "tableview1" with list of duration of tasks in the week, the selected day is in
          

#### `bt_dur_month_action(self, sender)`

  fill "tableview1" with list of duration of tasks in the month, the selected day is in
          

#### `bt_save_hours_action(self, sender)`

  save the content of the actual view of hours per day/week/month to csv.file
          

#### `seg_view_action(self, sender)`

  Manage selections in segmented control to chose view of second pane / right tableview
                  

#### `bt_save_all_action(self, sender)`

  Save all data to the .json and .csv files via memberfunctions of Titra.Calender
          

#### `bt_delete_all_action(self, sender)`

  DEPrICIATED 
  löschen +/- 70 Tage

#### `bt_backup_action(self, sender)`

  Sollte auch noch vorher alles löschen!
  und die globalen Variablen mit den Listen aller Projekte neu füllen
  
  BRAUCHE ICH die globalen Variablen noch?
  
  BRAUCHE ABER eine Methode Calender.clear()

#### `bt_read_all_action(self, sender)`

  DEPRECIATED
  Alle Daten aus den Standarddateien lesen
  NICHT vollständig realisiert!
  Sollte auch noch vorher alles löschen!
  und die globalen Variablen mit den Listen aller Projekte neu füllen

#### `bt_add_action(self, sender)`

  Füge eine neue Aktion hinzu und finde aus der aktuellen Selektion 
  den Task, die Task ID heraus. Action erstellen und an g_cal anfügen

#### `bt_delete_action(self, sender)`

  DEPRICIATED
  Lösche die selektierte Action aus dem Calender

#### `bt_now_action(self, sender)`

  Button now clicked, sets Datepicker to today()
                  

#### `dapi_action(self, sender)`

  Some Action in datepicker has happend
  update the content of "tableview1" according to new date

#### `bt_CopyPy_action(self, sender)`


#### `tv2_action(self, sender)`
`@ui.in_background`


#### `tv1_action(self, sender)`
`@ui.in_background`


#### `get_available_memory(self)`

  found in github
  what is the original source of this peace of magic?
  https://gist.github.com/lukaskollmer/a09c0278d2d224b9f4839a895ebb9988
  https://forum.omz-software.com/topic/3146/share-code-get-available-memory
      

#### `CopyFileList(filelist)`

  Kopiert Dateien aus ../TiTra/ nach ../TiTra.prod/ d.h. von Entwicklung nach Produktion
  noch ergänzen, dass das alter der Dateien getestet wird
  und ggf. den absoluten Pfad überprüfen
