# coding: utf-8
#
# TiTraPy.py
# 
# part of TiTraPy
# contains code for UI and initialization
#
# 21. Juni 2019

import console, os, ui
import datetime
from datetime import timedelta
from datetime import date

import random
#import json
import re
#import csv
import os
import sys
import shutil

import TiTra
import DataSources as MDS

from VersionInStatusBar import VersionInStatusBar
version = '00.7'
# VersionInStatusBar doesn't work! Why? TODO

# for get_available_memory
from ctypes import *
from objc_util import ObjCClass

class ShowTableView(object):
    def __init__(self):
        '''init UI, load pyui file
           keeps a list of messages for LogMessage(line:str) 

           self.selected_row
           self.state        wich view is activ? whats the content of the tableview
        '''
        self.view = ui.load_view('ShowTView')
        #self.view.name = 'ShowTableView'
        self.labelcounter = 0
        self.msglist=list()
        self.ui_lmsg=self.view['l_msg']
        self.state=0
        self.selected_row=-1
        self.selected=None
        
        self.view.present('fullscreen')        
        
# can't see any right_button_items!! why? Because this is a object not a ui.view
# but it has a view :-). self.view

        root, ext = os.path.splitext(sys.argv[0])  # script path without .py
        script_name = os.path.basename(root)  # script name without the path
        self.LogMessage(script_name)
        
        listOfDirs=root.split('/')
        l=len(listOfDirs)-1
        
        version_button = ui.ButtonItem()
        version_button.title = f"{listOfDirs[l-1]}/{listOfDirs[l]} V {version}"
        version_button.tint_color = 'red'
#        version_button.background_color=(1,1,0.90)
#        version_button.font=self.ui_lmsg.font
        print(f"feiner font in msg_log {self.ui_lmsg.font}")
#        version_button.action = self.clear_action
        self.view.right_button_items = [version_button]
        
        tv1 = self.view['tableview1']
        # print("\ntableview ...")
        # print(tv1.__dict__)
        tv1.row_height=24
        #tv1.font=('<system>',12)
        #tv1.data_source_font_size=12
        #tv1.data_source.font_size=12
        #tv1.data_source.data_source_font_size=12

        tv2 = self.view['tableview2']
        tv2.row_height=24        
                        
        # (font_name, font_size). In addition to regular font names, you can also use ('<system>',14) or '<system-bold>'
        
        # Button.font
        # The font for the button’s title as a tuple (font_name, font_size). In addition to regular font names, you can also
        # use '<system>' or '<system-bold>' to get the default regular or bold font.

        self.bt_task_action(None)        
        self.bt_cal2_action(None)        
        VersionInStatusBar(version=version)
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
        tv1.font=('<system>',12)
        self.get_available_memory()


    def bt_cal_action(self, sender):
        ''' fill "tableview1" with List of calender entries = actions
        '''
        now=self.view['datepicker'].date
        # datetime.datetime.today()
        
        dl=g_cal.UIActionsOfDayList(now)
        ''' TODO UI Actions umbauen, so dass die Komponenten einzeln im Dict sind'''
                
        #print(f"\nActionsOfDay {now}\n{dl}")
        # self.LogMessage(f"ActionsOfDay")

        lst = MDS.MyCalDataSource(g_cal.UIActionsOfDayList(now))
        tv1 = self.view['tableview1']
        tv1.data_source = tv1.delegate = lst
        tv1.data_source.delete_enabled = tv1.editing = False
        lst.action = self.tv2_action
        self.state=2
        self.selected_row=-1
        tv1.reload_data()
        self.get_available_memory()

    def bt_cal2_action(self, sender):
        ''' fill "tableview2" with list of calender entries = actions
        '''
        now=self.view['datepicker'].date
        # datetime.datetime.today()
        
        dl=g_cal.UIActionsOfDayList(now)
        lst = MDS.MyCalDataSource(g_cal.UIActionsOfDayList(now))
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
        self.view["datepicker"].font=("<system>",12)

        start=start.replace(hour=0, minute=0, second=0, microsecond=0)
        end=start+timedelta(days=1)  
                        
        lc=g_cal.findBetween(start, end)
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
        
        self.get_available_memory()
        if self.state==2 :
            self.save_cal_work()
        self.state=3
        
    def bt_dur_week_action(self,sender):
        ''' fill "tableview1" with list of duration of tasks in the week, the selected day is in
        '''
        start=self.view["datepicker"].date
        start=start.replace(hour=0,minute=0,second=0,microsecond=0)
        monday=start-timedelta(days=start.weekday())
        satday=monday+timedelta(days=5)
            
        lc=g_cal.findBetween(monday,satday)
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
        self.get_available_memory()
        if self.state==2 :
            self.save_cal_work()
        self.state=4
               
    def bt_dur_month_action(self, sender):
        ''' fill "tableview1" with list of duration of tasks in the month, the selected day is in
        '''
        start=self.view["datepicker"].date
        self.view["datepicker"].font=("<system>",12)

        mstart=start.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        mend=mstart+timedelta(weeks=0, days=32, hours=0, minutes=0, seconds=0)  
        mend=mend.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
                        
        lc=g_cal.findBetween(mstart, mend)
        l=lc.UICalcDurations()
                
        self.LogMessage(f"dur_month_action len {len(l)}")
        lst = MDS.MyDurDataSource("monthly",l)
        
        #lst.font=("<system>",12)
        lst.highlight_color=(1.0, 0.9, 0.3, 1.0)
# ListDataSource.font
# The font for displaying each row in the TableView. This is a 2-tuple of font name and size, e.g. ('<system>', 20).

# ListDataSource.highlight_color
# The highlight/selection color that the data source uses for the background of the cells that it’s creating.

# When setting this attribute, you can pass a string (CSS color name or hex, e.g. 'red' or '#ff0000'), a tuple 
# (e.g. (1.0, 0.0, 0.0, 0.5) for half-transparent red), or a number (e.g. 0.5 for 50% gray). Internally, all colors are 
# converted to RGBA tuples, so when you access the color later, 
# you’ll get (1.0, 1.0, 1.0, 1.0), no matter if you set the color to 'white', 
# '#ffffff' or just 1.0.        
        
        tv1 = self.view['tableview1']
        tv1.data_source = tv1.delegate = lst
        tv1.data_source.delete_enabled = tv1.editing = False
        self.selected_row=-1        
        tv1.reload_data()
        self.get_available_memory()
        if self.state==2 :
            self.save_cal_work()
        self.state=5

    def bt_save_all_action(self,sender) :
        """Alle Daten in die Standarddateien speichern
        """
# TODO Mehrere Backup Dateien behalten und mit Datum versehen
        if os.path.exists("tasks.json"):
            shutil.copy2("./tasks.json","./tasks.bak.json")
        with open('tasks.json', 'w') as f:
            TiTra.Task.WriteAllTasksToJSON(f)

        if os.path.exists("prj.json"):
            shutil.copy2("./prj.json","./prj.bak.json")
        with open('prj.json', 'w') as f:
            TiTra.Project.WriteAllProjectsToJSON(f)

        if os.path.exists("cal.csv"):
            shutil.copy2("./cal.csv","./cal.bak.csv")        
        with open("cal.csv", "w" ) as f:
            g_cal.WriteCalToCSV(f)
            
        self.LogMessage("Alles gespeichert: task.json, prj.json, cal.csv")
        print("Alles gespeichert: task.json, prj.json, cal.csv")
        
    def save_cal_work(self) :
        '''Speichert den Calender in cal.work.csv
           nachdem das stabil läuft, könnte auch direkt in den Originalkalender geschrieben werden
           NACHTEIL: sehr häufiges Schreiben, Fehleranfällig?'''

# TODO brauche ein dirtyflag, das nach Add / Delete gesetzt wird und nur dann wird wirklich der Kalender gespeichert        
        with open("cal.work.csv", "w" ) as f:
            g_cal.WriteCalToCSV(f)
        self.LogMessage("saved cal.work.csv")                    
            
        
    def bt_delete_all_action(self,sender) :
        """Alles löschen
           
           BRAUCHE ICH die globalen Variablen noch?
           
           BRAUCHE ABER eine Methode Calender.clear()
        """
        
        now=self.view["datepicker"].date
        
        g_cal.removeBetween(now-timedelta(days=70),now+timedelta(days=70))
        self.LogMessage(f"Alle Actions +/- 70 Tage {self.view['datepicker'].date} gelöscht")
        
    def bt_backup_action(self,sender) :
        """Sollte auch noch vorher alles löschen!
           und die globalen Variablen mit den Listen aller Projekte neu füllen
           
           BRAUCHE ICH die globalen Variablen noch?
           
           BRAUCHE ABER eine Methode Calender.clear()
        """
        
        now=self.view["datepicker"].date
        
        g_cal.SaveAndRemoveMonth(now,"./")
        self.LogMessage(f"SaveAndRemoveMonth {self.view['datepicker'].date}")
                                
    def bt_read_all_action(self,sender) :
        """Alle Daten aus den Standarddateien lesen
           NICHT vollständig realisiert!
           Sollte auch noch vorher alles löschen!
           und die globalen Variablen mit den Listen aller Projekte neu füllen
        """
        now=datetime.datetime.today()
        now=now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        g_cal.removeBetween(now,now+timedelta(days=40))
        
        with open('tasks.json', 'r') as f:
            all_tasks=TiTra.Task.ReadAllTasksFromJSON(f)
        with open('prj.json', 'r') as f:
            all_projects=TiTra.Project.ReadAllProjectsFromJSON(f)
        
        with open("cal.csv", "r" ) as f:
            g_cal.ReadCalFromCSV(f)
            
        self.LogMessage("NICHT gelöscht, alles gelesen: task.json, prj.json, cal.csv")
        
    def bt_InitTest_action(self, sender):
        InitForTest()
        self.bt_cal_action(sender)

    def bt_picture_action(self, sender):
        pass
        
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
            g_cal.add(task.NewAction(self.view["datepicker"].date))
            
#            self.bt_cal_action(sender)
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
            
            g_cal.removeBetween(time-timedelta(seconds=59),time+timedelta(seconds=59))
            
            self.bt_cal_action(sender)
            self.bt_cal2_action(sender)
                        
    def bt_save(self, sender):
        fn=self.view['t_fname'].text
        print (f"Save as {fn}")
        with open(fn, "w") as f :
            g_cal.WriteCalToCSV(f)
            
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
        label = self.view['l_date']
        label.text=sender.date.strftime("%d.%m.%Y")
        
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
	    CopyFileList(("ShowTView.py", "ShowTView.pyui", "NewTask.py", "VersionInStatusBar.py", "TiTra.py"))
	    self.LogMessage("Dateien von Entwicklung in Produktion kopiert")
	    
    def will_close(self):
        """ This will be called when a presented view is about to be dismissed.
        You might want to save data here.
        """
# TODO This never happens
#         
        print("\n\n***** Methode will_close called * * * * * * * * * *")    


	    
    @ui.in_background
    def tv2_action(self, sender):
        info = sender.items[sender.selected_row]
        self.selected=info
        self.selected_row=sender.selected_row
        self.LogMessage('selected_row {}'.format(sender.selected_row))
        
        # console.alert('info', 'selected_row {} = {}'.format(sender.selected_row, info))
        						
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
        
#        print('used:  ', mem_used)
#        print('free:  ', mem_free)
#        print('total: ', mem_total)
#        print('total (according to Cocoa): ', physical_memory)
        
        self.LogMessage(f"used {mem_used} free {mem_free} total {mem_total}")
        # NSProcessInfo.processInfo().activeProcessorCount()        




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

global g_cal
g_cal=TiTra.Calender()


# InitTaskProjects(False)
# DebugMiniAgenda(False)
# TiTra.ReadTasksProjects()

all_projects=dict()
all_task=dict()

with open('tasks.json', 'r') as f:
    all_tasks=TiTra.Task.ReadAllTasksFromJSON(f)
with open('prj.json', 'r') as f:
    all_projects=TiTra.Project.ReadAllProjectsFromJSON(f)

with open("cal.csv", "r" ) as f:
    g_cal.ReadCalFromCSV(f)


# print ("\nAlle Projekte:\n")    
# print(all_projects)
# print ("\nAlle Tasks:\n")    
# print(all_tasks)    



def InitForTest():
    now=datetime.datetime.today()
    now=now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    mlater=now+timedelta(weeks=0, days=32, hours=0, minutes=0, seconds=0)  
    mlater=mlater.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    
    print (f"\n*** Actions löschen zwischen {now} und {now+timedelta(days=40)}")
    
    g_cal.removeBetween(now,now+timedelta(days=40))
    
    print (f"\n*** Zufällig Tasks in diesen Monat füllen")
    print (f"Monatsstart = {now}")
    print (f"+1Monat     = {mlater}\n")
    
    zufallz=now.replace(hour=9, minute=0, second=0)
    
    for d in range (1,35) :
        t=TiTra.Task.FindTaskName("BL")
        
        if None != t :
            g_cal.add(t.NewAction(zufallz))
            
            for z in range(0,5) :
                zufallz= zufallz + timedelta(weeks=0, days=0, hours=0, minutes=30+random.randrange(50), seconds=3)  
                t=TiTra.Task.FindTaskid(random.randrange(10)+1)
                g_cal.add(t.NewAction(zufallz))
    
            t=TiTra.Task.FindTaskName("stopper")
    
            if None != t :
                zufallz=zufallz.replace(hour=18)
                g_cal.add(t.NewAction(zufallz))
    
        zufallz=zufallz.replace(hour=9, minute=0, second=0)
        zufallz=zufallz + timedelta(days=1, hours=0, minutes=1, seconds=0)  
           
    
print("\n\nShowTable View")
s=ShowTableView()
print(type(s))
if s != None :
    s.bt_save_all_action(None)
    
print("\n\n   Exit ShowTableView")
