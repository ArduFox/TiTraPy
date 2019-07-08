# coding: utf-8
#
# TiTraPy.py
# 
# part of TiTraPy
# contains code for UI and initialization
#
# Changes in V 00.74
# - Cleaing Up UI and showing some elements only if prefix in ("test", "DEV")
# - Button Save is aware of information shown in panel / tableview and changes title and saves appropriate data
#
# Changes in V 00.73
# - using the new Calender methods for reading and saving tasks, projects, calender
# - at the end of the file, the Calender instance will be set to prefix DEV. All saved files will therfore start with DEV.
# - coded sharing of hours .csv
# - TODO in TiTra.py Calender calculate hours and sort Output of CalcDurations
# - enabling / disabling buttons and hiding labels depending whats to see in right / second tableview
#
# Changes in V 00.72
# - using now a segemented control to change view in second pane
# - remaining code of VersionInStatusbar eliminated
# - Using custom view for main view to trap will_change() for saving the calender just before app exits
# - cleaning up the ui
# - added controls for saving and mailing calculated hours per day/week/month
# - added stubble of code to realy save the hours
# 
# Changes in V 00.71
# - added class variable myCalender in ShowTView, to contain the instance of TiTra.Calender
# - load TiTraPy.pyui
#
# Copyright?

#TODO error when deleting last action in day -- NOT ALWAYS -- not with id==0 ?? Maybe only when task.id = max??

# delete called! 0 6

# Traceback (most recent call last):
#  File "/private/var/mobile/Containers/Shared/AppGroup/24F5E5AD-C71D-4B25-92EF-6D14C753D158/Pythonista3/Documents/TiTra.prod/DataSources.py", line 280, in tableview_delete
#    self.myCalender.removeIDAtTime(a['id'] , time)
#  File "/private/var/mobile/Containers/Shared/AppGroup/24F5E5AD-C71D-4B25-92EF-6D14C753D158/Pythonista3/Documents/TiTra.prod/TiTra.py", line 521, in removeIDAtTime
#    return self.__actions[i]
#IndexError: list index out of range

import console, os, ui
import datetime
from datetime import timedelta
#from datetime import date

#import random
#import json
#import re
#import csv
#import os
import sys
import shutil

import TiTra
import DataSources as MDS

version = '00.74'

# for get_available_memory
from ctypes import *
from objc_util import ObjCClass

#import ui

class MyView (ui.View):
    '''from pythonista ui documentation
       I need it to implement will_close() to save the data when ui is exited
       
       Lessons learned
       - ui.loadview is not a method of View but returns a View instance!!
       - View is the only ui class that can be subclassed - tells the doc
       - How can I load a pyui file in my own class
         In the GUI Editor use the field Custom View Class at the bottom
         
       - See https://forum.omz-software.com/topic/989/any-ui-module-tutorials-out-there/29
       - there are best practice rules in that thread
       - and a tutorial  
    '''
    
    def __init__(self):
        # This will also be called without arguments when the view is loaded from a UI file.
        # You don't have to call super. Note that this is called *before* the attributes
        # defined in the UI file are set. Implement `did_load` to customize a view after
        # it's been fully loaded from a UI file.
        self.cal=None
        pass
        
    def setCalender(self, cal:TiTra.Calender):
        
        self.cal=cal

    def did_load(self):
        # This will be called when a view has been fully loaded from a UI file.
        pass

    def will_close(self):
        # This will be called when a presented view is about to be dismissed.
        # You might want to save data here.
        
        
        print("My_View.will_close saving Calender at ",datetime.datetime.now().strftime("%H:%M:%S"))
        if None != self.cal :
            cal.SaveCal()
#            print("Calender gespeichert: cal.csv")
            self.CalChanged=False                        

    def draw(self):
        # This will be called whenever the view's content needs to be drawn.
        # You can use any of the ui module's drawing functions here to render
        # content into the view's visible rectangle.
        # Do not call this method directly, instead, if you need your view
        # to redraw its content, call set_needs_display().
        # Example:
        # path = ui.Path.oval(0, 0, self.width, self.height)
        # ui.set_color('red')
        # path.fill()
        # img = ui.Image.named('ionicons-beaker-256')
        # img.draw(0, 0, self.width, self.height)
        pass

    def layout(self):
        # This will be called when a view is resized. You should typically set the
        # frames of the view's subviews here, if your layout requirements cannot
        # be fulfilled with the standard auto-resizing (flex) attribute.
        pass

    def touch_began(self, touch):
        # Called when a touch begins.
        pass

    def touch_moved(self, touch):
        # Called when a touch moves.
        pass

    def touch_ended(self, touch):
        # Called when a touch ends.
        pass

    def keyboard_frame_will_change(self, frame):
        # Called when the on-screen keyboard appears/disappears
        # Note: The frame is in screen coordinates.
        pass

    def keyboard_frame_did_change(self, frame):
        # Called when the on-screen keyboard appears/disappears
        # Note: The frame is in screen coordinates.
        pass


class ShowTableView(object):
    def __init__(self, cal:TiTra.Calender):
        '''init UI, load pyui file
           keeps a list of messages for LogMessage(line:str) 

           self.selected_row
           self.state        which view is activ? whats the content of the second / right tableview
        '''
        self.view = ui.load_view('TiTraPy.pyui')
        self.labelcounter = 0
        self.msglist=list()
        self.ui_lmsg=self.view['l_msg']
        self.state=0
        self.selected_row=-1
        self.selected=None
        self.myCalender=cal
        self.CalChanged=False
        
        self.view.setCalender(self.myCalender)
        
        self.view.present('fullscreen')        
        
        root, ext = os.path.splitext(sys.argv[0])  # script path without .py
        script_name = os.path.basename(root)  # script name without the path
        self.LogMessage(script_name)
        
        listOfDirs=root.split('/')
        l=len(listOfDirs)-1
        pre=self.myCalender.GetPrefix()
        if pre in ("test", "DEV") :
            pass
        else:
            self.view["bt_BackupMonth"].hidden=True
            self.view["bt_save_all"].hidden=True
            self.view["bt_CopyPy"].hidden=True
                                            
        version_button = ui.ButtonItem()
        version_button.title = f"{listOfDirs[l-1]}/{listOfDirs[l]} V {version} : {pre}"
        version_button.tint_color = 'red'
#        version_button.background_color=(1,1,0.90)
#        version_button.font=self.ui_lmsg.font
#        print(f"feiner font in msg_log {self.ui_lmsg.font}")
#        version_button.action = self.clear_action
        self.view.right_button_items = [version_button]
        
        tv1 = self.view['tableview1']
        # print("\ntableview ...")
        # print(tv1.__dict__)
        tv1.row_height=26
 
        tv2 = self.view['tableview2']
        tv2.row_height=26        
                        
        # (font_name, font_size). In addition to regular font names, you can also use ('<system>',14) or '<system-bold>'
        
        # Button.font
        # The font for the button’s title as a tuple (font_name, font_size). In addition to regular font names, you can also
        # use '<system>' or '<system-bold>' to get the default regular or bold font.

        self.bt_task_action(None)        
        self.bt_cal2_action(None)                
        self.LogMessage("init done.")

                        
    def LogMessage(self,line:str) :
        '''log a message to large label to show the user / developer what happend
        '''

        #print(f"Listenlänge {len(self.msglist)}. Textlänge {len(self.ui_lmsg.text)}")
        if len(self.msglist) > 7:
        # or len(self.ui_lmsg.text) > 100:
            # print("pop msglist")
            self.msglist.pop(0)
            
            # pop löscht das letzte Element

        nowstr=datetime.datetime.today().strftime("%H:%M:%S : ")
        self.msglist.append(nowstr + line)
        self.ui_lmsg.text="\n".join(self.msglist)

    def bt_empty_action(self, sender):
        '''clear tableview1
        '''
        tv1 = self.view['tableview1']
        tv1.data_source = tv1.delegate = ui.ListDataSource([])
        tv1.data_source.delete_enabled = tv1.editing = False
        tv1.reload_data()
        self.view['bt_save_hours'].enabled=False
        self.view['bt_add'].enabled=False

    def bt_task_action(self, sender):
        ''' fill "tableview1" with List of Tasks
        '''
        lst = MDS.MyTaskDataSource(TiTra.Task.UITasksList())
        #print(f"\nShow tasks {TiTra.Task.UITasksList()}")
        tv1 = self.view['tableview1']
        tv1.data_source = tv1.delegate = lst
        tv1.data_source.delete_enabled = tv1.editing = False
        lst.action = self.tv2_action
        self.state=1
        self.selected_row=-1
        tv1.reload_data()
#        tv1.font=('<system>',12)
        self.view['bt_add'].enabled=True
#        self.view['bt_save_hours'].enabled=False
        self.view['bt_save_hours'].title="Save Cal"        
        self.view['label_up'].hidden=False
        self.view['label_left'].hidden=False        
        self.get_available_memory()


    def bt_cal2_action(self, sender):
        ''' fill "tableview2" with list of calender entries = actions
        '''
        now=self.view['datepicker'].date
        # datetime.datetime.today()
        
        dl=self.myCalender.UIActionsOfDayList(now)
        lst = MDS.MyCalDataSource(self.myCalender, self.myCalender.UIActionsOfDayList(now))
        tv2 = self.view['tableview2']
        tv2.data_source = tv2.delegate = lst
        tv2.data_source.delete_enabled = tv2.editing = False
        lst.action = self.tv2_action
#        self.state=2
#        self.selected_row=-1
        tv2.reload_data()
        self.get_available_memory()

    def bt_dur_day_action(self, sender):
        ''' fill "tableview1" with list of duration of tasks in selcted day
        Anzeigen welche Zeiten für welche Tasks gebraucht wurden
        '''
        start=self.view["datepicker"].date

        start=start.replace(hour=0, minute=0, second=0, microsecond=0)
        end=start+timedelta(days=1)  
                        
        lc=self.myCalender.findBetween(start, end)
        l=lc.UICalcDurations()
        
        self.LogMessage(f"dur_day_action len {len(l)}")
            
        #self.LogMessage(f"dur_day_action liste {len(l)}")    
        lst = MDS.MyDurDataSource("daily",l)
        lst.highlight_color=(1.0, 0.9, 0.3, 1.0)        
        tv1 = self.view['tableview1']
        tv1.data_source = tv1.delegate = lst
        tv1.data_source.delete_enabled = tv1.editing = False
        self.selected_row=-1        
        tv1.reload_data()
        self.view['bt_save_hours'].enabled=True
        if self.state==2 :
            self.view['bt_save_hours'].title="Save Hours"                
        self.view['bt_add'].enabled=False
        self.view['label_up'].hidden=True
        self.view['label_left'].hidden=True
        self.state=3
        
    def bt_dur_week_action(self,sender):
        ''' fill "tableview1" with list of duration of tasks in the week, the selected day is in
        '''
        start=self.view["datepicker"].date
        start=start.replace(hour=0,minute=0,second=0,microsecond=0)
        monday=start-timedelta(days=start.weekday())
        satday=monday+timedelta(days=5)
            
        lc=self.myCalender.findBetween(monday,satday)
        l=lc.UICalcDurations()
        
        self.LogMessage(f"dur_week_action len {len(l)} {monday.strftime('%a %d.%m.%y')}")
            
        #self.LogMessage(f"dur_day_action liste {len(l)}")    
        lst = MDS.MyDurDataSource("weekly",l)
        lst.highlight_color=(1.0, 0.9, 0.3, 1.0)
        tv1 = self.view['tableview1']
        tv1.data_source = tv1.delegate = lst
        tv1.data_source.delete_enabled = tv1.editing = False
        self.selected_row=-1        
        tv1.reload_data()
        self.view['bt_save_hours'].enabled=True
        if self.state==2 :
            self.view['bt_save_hours'].title="Save Hours"                        
        self.view['bt_add'].enabled=False
        self.view['label_up'].hidden=True
        self.view['label_left'].hidden=True        
        self.state=4
               
    def bt_dur_month_action(self, sender):
        ''' fill "tableview1" with list of duration of tasks in the month, the selected day is in
        '''
        start=self.view["datepicker"].date
#        self.view["datepicker"].font=("<system>",12). # WHAT is THIS ??

        mstart=start.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        mend=mstart+timedelta(weeks=0, days=32, hours=0, minutes=0, seconds=0)  
        mend=mend.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
                        
        lc=self.myCalender.findBetween(mstart, mend)
        l=lc.UICalcDurations()
                
        self.LogMessage(f"dur_month_action len {len(l)}")
        lst = MDS.MyDurDataSource("monthly",l)
        
        #lst.font=("<system>",12)
        lst.highlight_color=(1.0, 0.9, 0.3, 1.0)
        tv1 = self.view['tableview1']
        tv1.data_source = tv1.delegate = lst
        tv1.data_source.delete_enabled = tv1.editing = False
        self.selected_row=-1        
        tv1.reload_data()
        self.view['bt_save_hours'].enabled=True
        if self.state==2 :        
            self.view['bt_save_hours'].title="Save Hours"                        
        self.view['bt_add'].enabled=False
        self.view['label_up'].hidden=True
        self.view['label_left'].hidden=True        
        self.state=5
        
    def bt_save_hours_action(self, sender):
        '''save the content of the actual view of hours per day/week/month to csv.file
        '''
        
        start=self.view["datepicker"].date
                    
        if self.state==5 :  # month
            mstart=start.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            mend=mstart+timedelta(weeks=0, days=32, hours=0, minutes=0, seconds=0)  
            mend=mend.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
                            
            lc=self.myCalender.findBetween(mstart, mend)            
            self.LogMessage(f"save week of {mstart.strftime('%a %d.%m.%y')}")
            fname=f"{mstart.strftime('%y-%m-%d')}_month_hours.csv"
                
        elif self.state==4: # week
            start=start.replace(hour=0,minute=0,second=0,microsecond=0)
            monday=start-timedelta(days=start.weekday())
            satday=monday+timedelta(days=5)
                
            lc=self.myCalender.findBetween(monday,satday)
            
            self.LogMessage(f"save week of {monday.strftime('%a %d.%m.%y')}")        
            fname=f"{monday.strftime('%y-%m-%d')}_week_hours.csv"
                        
        elif self.state==3: #day
            start=start.replace(hour=0,minute=0,second=0,microsecond=0)
            end=start+timedelta(days=1)                  
            
            lc=self.myCalender.findBetween(start,end)
            
            self.LogMessage(f"save day of {start.strftime('%a %d.%m.%y')}")
            fname=f"{start.strftime('%y-%m-%d')}_day_hours.csv"
                    
        else :
            self.LogMessage(f"saving the calender")                 
            self.myCalender.SaveCal()            
            return
                  
        with open(fname,"w") as f:
            lc.WriteDurationsToCSV(f)        

        self.LogMessage(f"File {fname} with hours written")
        if self.view['switch_share_hours'].value:
            console.open_in(fname)
        
        # check if mail hours is set, then generate email with file as attachement
                        
                                                
    def seg_view_action(self,sender):
        '''Manage selections in segmented control to chose view of second pane
        '''
        i = self.view['segmentedcontrol'].selected_index
        if i == 0:
            self.bt_task_action(None)
        elif i == 1:
            self.bt_dur_day_action(None)    		
        elif i == 2:
            self.bt_dur_week_action(None)    		
        elif i == 3:
            self.bt_dur_month_action(None)    		

            
                        
                                                
    def bt_save_all_action(self,sender) :
        """Alle Daten in die Standarddateien speichern
        """
# TODO Mehrere Backup Dateien behalten und mit Datum versehen
# TODO move Code to class calender, maintain a prefix for the files in each instance of calender
        self.myCalender.SaveTasks()
        self.myCalender.SaveProjects()
        self.myCalender.SaveCal()

        self.LogMessage("Alles gespeichert: task.json, prj.json, cal.csv")
        print("Alles gespeichert: task.json, prj.json, cal.csv ",datetime.datetime.now().strftime("%H:%M:%S"))
                                
    def save_cal_work(self) :
        ''' DEPRECIATED
           Speichert den Calender in cal.work.csv
           nachdem das stabil läuft, könnte auch direkt in den Originalkalender geschrieben werden
           NACHTEIL: sehr häufiges Schreiben, Fehleranfällig?'''

# TODO brauche ein dirtyflag, das nach Add / Delete gesetzt wird und nur dann wird wirklich der Kalender gespeichert        
        with open("cal.work.csv", "w" ) as f:
            self.myCalender.WriteCalToCSV(f)
        self.LogMessage("saved cal.work.csv")                    
            
        
    def bt_delete_all_action(self,sender) :
        """Alles löschen
           
           BRAUCHE ICH die globalen Variablen noch?
           
           BRAUCHE ABER eine Methode Calender.clear()
        """
        
        now=self.view["datepicker"].date
        
        self.myCalender.removeBetween(now-timedelta(days=70),now+timedelta(days=70))
        self.LogMessage(f"Alle Actions +/- 70 Tage {self.view['datepicker'].date} gelöscht")
        
    def bt_backup_action(self,sender) :
        """Sollte auch noch vorher alles löschen!
           und die globalen Variablen mit den Listen aller Projekte neu füllen
           
           BRAUCHE ICH die globalen Variablen noch?
           
           BRAUCHE ABER eine Methode Calender.clear()
        """
        
        now=self.view["datepicker"].date
        
        self.myCalender.SaveAndRemoveMonth(now,"./")
        self.LogMessage(f"SaveAndRemoveMonth {self.view['datepicker'].date}")
                                
    def bt_read_all_action(self,sender) :
        """DEPRECIATED
           Alle Daten aus den Standarddateien lesen
           NICHT vollständig realisiert!
           Sollte auch noch vorher alles löschen!
           und die globalen Variablen mit den Listen aller Projekte neu füllen
        """
        return
        now=datetime.datetime.today()
        now=now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        self.myCalender.removeBetween(now,now+timedelta(days=40))
        
        with open('tasks.json', 'r') as f:
            all_tasks=TiTra.Task.ReadAllTasksFromJSON(f)
        with open('prj.json', 'r') as f:
            all_projects=TiTra.Project.ReadAllProjectsFromJSON(f)
        
        with open("cal.csv", "r" ) as f:
            self.myCalender.ReadCalFromCSV(f)
            
        self.LogMessage("NICHT gelöscht, alles gelesen: task.json, prj.json, cal.csv")
        
    def bt_add_action(self,sender) :
        """Füge eine neue Aktion hinzu und finde aus der aktuellen Selektion 
           den Task, die Task ID heraus. Action erstellen und an g_cal anfügen
        """
        self.LogMessage(f"add sel={self.selected_row} in state {self.state}")
        
        if self.state == 1 and self.selected_row!=-1 :
            tv1 = self.view['tableview1']
            a=self.selected
            
            self.LogMessage(f"{a}")
            
            id=int(a["id"])
            task=TiTra.Task.FindTaskid(id)
            self.myCalender.add(task.NewAction(self.view["datepicker"].date))
            self.CalChanged=True
            
            # TODO set flag to True if an Delete has ocurred -> in DataSources.py
            # TODO Save Calender (no method to save the calender alone) if Flag is True! When??
    		# not a good design! 
    		# this class already knows the calender -> the calender not the UI should be aware if there were changes, that need saving            
            
#            self.bt_cal_action(sender)
            print("add_action ",datetime.datetime.now().strftime("%H:%M:%S"))
            self.bt_cal2_action(sender)
            
                    
    def bt_delete_action(self, sender) :
        """Lösche die selektierte Action aus dem Calender
           enthält das dict auch die zeit in geeigneter Form?
           g_cal kann removeBetween(fro,til)
        """
        self.LogMessage(f"delete sel={self.selected_row} in state {self.state}")
        
        if self.state == 2 and self.selected_row!=-1 :
            tv1 = self.view['tableview1']
            a=self.selected
            
            self.LogMessage(f"{a['date']} {a['time']} {a['title']}")        
            #print(a)
            
            time=datetime.datetime.strptime(f"{a['date']} {a['time']}", "%Y-%m-%d %H:%M")
            
            self.LogMessage(time.strftime("%d.%m.%Y %H:%M:%S"))
            
            self.myCalender.removeBetween(time-timedelta(seconds=59),time+timedelta(seconds=59))
            
            self.bt_cal_action(sender)
            self.bt_cal2_action(sender)
                        
    def bt_save(self, sender):
        fn=self.view['t_fname'].text
        print (f"Save as {fn}")
        with open(fn, "w") as f :
            self.myCalender.WriteCalToCSV(f)
            
        label2=self.view['save_done']
        if label2 :    
            self.view.remove_subview(label2)
                    
        label2 = ui.Label(name='save_done')
        label2.text = "saved at "+ datetime.datetime.today().strftime("%H:%M:%S") 
        label2.x = 655
        label2.y = 380
        label2.width = 200
        
        self.LogMessage(f"Calender saved as {fn}")
        self.view.add_subview(label2)

    def tipi_action(self,sender):
        pass
			
    def bt_now_action(self,sender):
        '''Button now clicked, sets Datepicker to today()
        '''
        label = self.view['l_date']
        d=datetime.datetime.today()
        self.view["datepicker"].date=d
        label.text=d.strftime("%d.%m.%Y")
                
        if self.state == 2 :
            self.bt_cal_action(sender)
        elif self.state == 3 :
            self.bt_dur_day_action(sender)
        elif self.state == 4 :
            self.bt_dur_week_action(sender)
        elif self.state == 5 :
            self.bt_dur_month_action(sender)
        self.bt_cal2_action(sender)
                    
    def dapi_action(self,sender):
        '''Some Action in datepicker has happend
           update the content of "tableview1" according to new date
        '''
        # print(f"\n Gewähltes Datum {sender.date}")
        # Wichtig hier in der zugehörigen View anhand des Namens die Subview finden!
        
        if self.state == 2 :
            self.bt_cal_action(sender)
        elif self.state == 3 :
            self.bt_dur_day_action(sender)
        elif self.state == 4 :
            self.bt_dur_week_action(sender)
        elif self.state == 5 :
            self.bt_dur_month_action(sender)
        self.bt_cal2_action(sender)
                        
		# Anderes Popup für die ersten Listen
		# sender.selected_row enthält den Index des gewählten Eintrags
		# und sender.items eine Liste aller Einträge
		# kann ich wie in picture_actions neben definierten keys auch eigene verwenden und danach darauf zugreifen?
		# Ja das geht ohne zu 

    def bt_CopyPy_action(self,sender):
	    CopyFileList(("TiTra.py", "TiTraPy.py", "DataSources.py", "TiTraPy.pyui"))
	    self.LogMessage("Dateien von Entwicklung in Produktion kopiert")
	    
	    
    @ui.in_background
    def tv2_action(self, sender):
        info = sender.items[sender.selected_row]
        self.selected=info
        self.selected_row=sender.selected_row
        self.LogMessage('selected_row {}'.format(sender.selected_row))
        
    @ui.in_background
    def tv1_action(self, sender):
        info = sender.items[sender.selected_row]
        console.alert('info', '\n'.join(['{} = {}'.format(i, info[i]) for i in info]))

    def get_available_memory(self): 
        """found in github
            what is the original source of this peace of magic?
            https://gist.github.com/lukaskollmer/a09c0278d2d224b9f4839a895ebb9988
            https://forum.omz-software.com/topic/3146/share-code-get-available-memory
        """

        NSProcessInfo = ObjCClass('NSProcessInfo')
        NSByteCountFormatter = ObjCClass('NSByteCountFormatter')
        
        class c_vm_statistics(Structure):
        	_fields_ = [('free_count', c_uint),
        	('active_count', c_uint),
        	('inactive_count', c_uint),
        	('wire_count', c_uint),
        	('zero_fill_count', c_uint),
        	('reactivations', c_uint),
        	('pageins', c_uint),
        	('pageouts', c_uint),
        	('faults', c_uint),
        	('cow_faults', c_uint),
        	('lookups', c_uint),
        	('hits', c_uint),
        	('purgeable_count', c_uint),
        	('purges', c_uint),
        	('speculative_count', c_uint)]
    	
        c = cdll.LoadLibrary(None)
        
        mach_host_self = c.mach_host_self
        mach_host_self.restype = c_uint
        mach_host_self.argtypes = [c_void_p]
        
        host_page_size = c.host_page_size
        host_page_size.restype = c_int
        host_page_size.argtypes = [c_uint, POINTER(c_uint)]
        
        host_statistics = c.host_statistics
        host_statistics.restype = c_int
        host_statistics.argtypes = [c_uint, c_int, POINTER(c_int), POINTER(c_uint)]
        
        host_port = c_uint()
        host_size = c_uint()
        page_size = c_uint()
        
        host_port = mach_host_self(None)
        host_size = c_uint(int(sizeof(c_vm_statistics) / sizeof(c_int)))
        host_page_size(host_port, byref(page_size))
        vm_stat = c_vm_statistics()
        
        HOST_VM_INFO = c_int(2) # This is a c macro
        KERN_SUCCESS = 0 # Another c macro (No c_int initializer used because we don't pass it to a c function)
        
        get_host_statistics = host_statistics(host_port, HOST_VM_INFO, cast(byref(vm_stat), POINTER(c_int)), byref(host_size))
        
        if not get_host_statistics == int(KERN_SUCCESS):
        	print("Failed to fetch vm statistics")
        	
        mem_used = (vm_stat.active_count +
                                                        vm_stat.inactive_count +
                                                        vm_stat.wire_count) * int(page_size.value)
        mem_free = vm_stat.free_count * int(page_size.value)
        mem_total = mem_used + mem_free
        
        physical_memory = NSProcessInfo.processInfo().physicalMemory()
        
        byteCountFormtter = NSByteCountFormatter.new()
        mem_used = byteCountFormtter.stringFromByteCount_(mem_used)
        mem_free = byteCountFormtter.stringFromByteCount_(mem_free)
        mem_total = byteCountFormtter.stringFromByteCount_(mem_total)
        physical_memory = byteCountFormtter.stringFromByteCount_(physical_memory)
        
        self.LogMessage(f"used {mem_used} free {mem_free} total {mem_total}")



# ======= End of Class ShowTView ===============================================


def CopyFileList(filelist):
    """Kopiert Dateien aus ../TiTra/ nach ../TiTra.prod/ d.h. von Entwicklung nach Produktion
       noch ergänzen, dass das alter der Dateien getestet wird
       und ggf. den absoluten Pfad überprüfen
    """
    #filelist=( "ShowTableView.py", "ShowTableView.pyui", "ScrollView.py", "NewTask.py" )
    todir='../TiTra.prod/'
    fromdir='../TiTra/'
    
    if not os.path.exists(fromdir):
        print(f"{fromdir} existiert leider nicht")
    else:    
    	
    	for fi in filelist :
    	    
    	    print(f"copy {fi}           >> from {fromdir} to {todir}")
    	    
    	    shutil.copy2(fromdir+fi,todir+fi)




global cal        

if os.path.exists("prefix.txt"):
    with open("prefix.txt","r") as f:
        prefix=f.readline()[0:-1]
#    print (f"\n** prefix.txt gefunden prefix='{prefix}'\n") 
    cal=TiTra.Calender(prefix)
else :    
    cal=TiTra.Calender("DEV")

# here can result a problem, if done in other sequence
cal.LoadTasks()
cal.LoadProjects()
cal.LoadCal()

s=ShowTableView(cal)

