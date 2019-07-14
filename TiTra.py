#!/usr/bin/python
#
# PyTiTra_Classes.py
#
# Implements classes with "bussiness logic" and data modell for Time Tracking
#
# No GUI Implementation and not depended on IOS pythonista. Works and is tested in python and Jupyter Notebook

# https://realpython.com/documenting-python-code/#why-documenting-your-code-is-so-important

import pprint

import datetime
from datetime import timedelta
from datetime import date

import os, shutil



import random
import json
import re
import csv


class Task:
    'Beschreibt eine Tätigkeit bzw. Teilprojekt bzw. Aufgabe, die zu konkreten Zeiten getand werden kann bzw. auf die Zeiten gebucht werden können'


    # Soll ich hier eine statische Liste aller tasks führen?
    # Dann könnte ich die hier lesen & finden
    # mindestens für Debugging

    __task_num=0
    __all_tasks=dict()

    def __init__(self, name : str, emoij="X" , farbe="#265B6A" ):
        'Neuen Task anlegen und im Dictionary aller tasks aufnehmen'
        self._name=name
        self._emoij=emoij
        self._farbe=farbe
        self._projectName=""
        self._project=None             # 0 oder none ??
        self._id=Task.__task_num
        Task.__task_num += 1
        self.__all_tasks[self._id]=self

    def __str__(self):
        return "Task ([%d]: %s, %s, %s, %s)" % (self._id, self._name, self._emoij, self._farbe, self._projectName)

    def SetProject(self,prj):
        """Projektnamen eintragen oder ändern.
          Hier wird geprüft, ob das Projekt sich ändert und in diesem
          Fall wird der Task aus dem anderen Projekt entfernt werden"""

#        if self._project != 0 :

        if self._project != None :
            # print("\n\n~~~~ PROBLEM Verschiebe Task zwischen Projekten von  {} nach {} ~~~~\n".format(self._project._name,prj._name))
            # print ("** Task.SetProject {}".format(prj._name))
            # print (f"**   projektName = {self._projectName} projekt = ")
            self._project.removeTask(self)              #  TODO not yet tested
            
        self._projectName=prj._name
        self._project=prj
        'TODO Sollte hier wirklich __project.addTask ausgeführt werden? Wie ist die "normale" Aufruf Kaskade?'
        self._project.addTask(self)                     # TODO 
        
    def SetName(self,NewName) :
        'Name des Tasks ändern'
        # in Projekt wird aufgrund der Referenz auf den Task der neue Name angezeigt
        # in Calender aber nicht, weil keine Referenz
        # und in Projekt ändert sich der key im dict auch nicht :-(
        # print ("** Task.SetName '{}'".format(NewName))
        # print (f"**   projektName = {self._projectName} projekt = ")

#        if self._project != 0 :
        if self._project != None :
            # print("\n\n~~~~ PROBLEM Ändere Namen '{}' ~~~~\n".format(NewName))
            self._project.removeTask(self)              #  TODO not yet tested
            self._name=NewName
            self._project.addTask(self)
        else :
            self._name=NewName
        

    @classmethod
    def NextID(cls):
        'Gibt die nächste ID-Nummer zurück, die für den nächsten Task vergeben wird'
        return Task.__task_num

    @classmethod
    def FindTaskid(cls,id) :
        'Finde den Task mit der <id>'
        'return'
        '  None falls nichts gefunden wurde'
        return cls.__all_tasks[id]

    @classmethod
    def FindTaskName(cls,name) :
        'Finde den ERSTEN Task mit dem <name>'
        'return'
        '  None falls nichts gefunden wurde'

        for k,_t in cls.__all_tasks.items() :
            if name == _t._name :
                return _t

        return None

    @classmethod
    def RemoveTaskid(cls,id) :
        'Einen Task anhand seiner id entfernen und löschen'
        'noch nicht implementiert'

        print(f"\nRemoveTaskid({id})  NOT YET IMPLEMENTED!\n")
        help(cls.RemoveTaskid)

    @classmethod
    def AllTasksStr(cls)->str :
        """Alle Tasks, die es gibt ausgeben
        return
            String mit allen Tasks
        """

        s="AllTasksStr:"
        for k,_t in cls.__all_tasks.items() :
            s=s+f"\n{k}: {_t}"
        return s

    @classmethod
    def GetAllTasksList(cls) ->list:
        """Return the List of AllTasks __all_tasks
        """
        return cls.__all_tasks
      
    @classmethod
    def UITasksList(cls) ->list:
        """Alle Tasks, die es gibt als UI angenehme Liste ausgeben
        return
            list of dict of all tasks
        """

        l=list()
        for k,_t in cls.__all_tasks.items() :
            l.append({"titl":f"{_t._name} '{_t._emoij}' [{_t._projectName}]", 'id':f"{_t._id}",
            "task":_t._name,
            'prj': _t._projectName,
            'color': _t._farbe,
            'id':_t._id
            })
        l=sorted(l, key = lambda i: (i['prj'], i['task'])) 
        return l

    def NewAction(self,time) :
        'Neue Action mit definierter Zeit anlegen'
        act = Action(self,time)       
        return act

    def StartActionNow(self) :
        'Neue Action jetzt anlegen'
        act = Action(self,datetime.datetime.now())       
        return act

    @classmethod
    def StopAction(cls,time) :
        """stopper Action mit definierter Zeit  anlegen um eine Aktivität zu beenden 
              return
                angelegte Action oder
                None, falls Task mit id=0 nicht gefunden wurde
                wäre 0 im Fehlerfall ein besserer Rückgabecode? TODO """

        _s=Task.FindTaskid(0)

        if None != _s :
            act = _s.NewAction(time) 
            return act
        else :
            print("\nERROR\n     StopAction with _od==0 not found!\n")
            'Hier sollte ich eigentlich einen Fehler anzeigen'

        return None


    # return data representation for JSON object
    def attr_dict(self):
        'Kopiert und ändert das dict mit den Attributen der Klasse, so dass JSON damit klar kommt'

        # VORSICHT in python ist eine Zuweisung kein Kopieren eines Objectes in eine neue Instanz!
        odict = self.__dict__.copy()    # get attribute dictionary
#        print(odict)
        del odict['_project']    # remove reference to project
        return odict

    @classmethod
    def WriteAllTasksToJSON(cls,filehandle) -> str:
        'Schreibt alle Tasks in eine Datei - Bereits doppeltes Schreiben in Dateien entfernt'
        'return'
        '   JSON String In der aktuellen Arbeitsversion '

        JSONstr=""
        out_dict=dict()

        for _id, _t in cls.__all_tasks.items() :

            out_dict[_t._id]=_t.attr_dict()
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
    def ReadAllTasksFromJSON(cls, filehandle) :
        """Liest Tasks aus einer JSON Datei ein und legt diese an
           return
           Dictionary of new generated Tasks"""

        jdict=dict()

        jdict=json.load(filehandle)

        # Eigentlich davor alle Tasks löschen!

        new_tasks=dict()
        max_id=0
        nt=None

        for _id, _t in jdict.items() :
            nt=Task(_t["_name"], _t["_emoij"], _t["_farbe"])
            nt._id=_t["_id"]
            new_tasks[_t["_id"]]=nt
            # print(f"{_t['_id']}: {nt}")
            max_id=max(nt._id,max_id)  # TODO 

        if Task.NextID() <= max_id :
            print(f"\nReadAllTasksFromJSON: max_id={max_id} > .NextID() !! \n")

        #print("\n ** ReadAllTasksFromJSON  newtasks")
        #pp.pprint(new_tasks)

        #print("\n **   __all_tasks")
        #pp.pprint(cls.__all_tasks)

        return new_tasks

    @classmethod
    def DeleteAllTasks(cls) :
        for _id, _t in cls.__all_tasks.items() :
            pass
            # _t.delete() geht auch nicht

            #delete(_t) geht nicht

            # wie lösche ich objekte
        
        cls.__all_tasks.clear()
        cls.__task_num=0


    @classmethod
    def CopyDictAllTasks(cls) -> dict :
        """ Erstellt eine Kopie des internen Dictionarys über alle tasks
            return
                dict with all tasks
        """
        return cls.__all_tasks.copy()


class Project:
    'Beschreibt ein Projekt, zu dem mehrere Taten gehören können'

    __all_projects=dict()

    def __init__(self, name : str, emoij="X" , farbe="#265B6A"  ):
        self._name=name
        self._emoij=emoij
        self._farbe=farbe
        self.__tasks=dict()
        self.__all_projects[name]=self


    # __tasks ist von aussen nicht sichtbar
    # _tasks wäre read only
    # alle anderen Atrribute können von außen zugegriffen werden

    def addTask(self,task):
        'Fügt einen Task zu einem Project hinzu, d.h. ein weiterer Eintrag im Dictionary. KEINE CHECKS'
        if None != task :
            self.__tasks[task._name]=task
            if task._project == None :
                task.SetProject(self) 

    def removeTask(self,task):
        'Löscht einen Task aus einem Project KEINE CHECKS'
        'https://realpython.com/python-dicts/'

        # https://realpython.com/python-dicts/
        self.__tasks.pop(task._name,"")

    def __str__(self):
        return "Project({}, {}, {} \n {} )".format(self._name, self._emoij, self._farbe, self.__tasks)

    def print_tasks(self):
        'Hübscher Ausdruck aller Tasks im Project'

        for k, t in self.__tasks.items():
            print(f"Task : {k} <{t._emoij}>  prj={t._projectName}")

    def UITasksList(self) ->list:
        """UI freundliche Liste mit allen Tasks als String erstellen
            return
                list of dicts of strings of all tasks of this project
        """
        
        l=list()
        for k, _t in self.__tasks.items():
            l.append({"titl":f"{_t._name} '{_t._emoij}' [{_t._projectName}]", 'id':f"{_t._id}",
            "name":_t._name,
            'prj': _t._projectName,
            'color': _t._farbe,
            'id':_t._id
            })

        l=sorted(l, key = lambda i: (i['prj'], i['name'])) 
        return l

    def find_task(self,key) :
        'Fíndet eine Task des Projektes anhand seines Namens'
        return self.__tasks[key]

    def len(self) -> int:
        'return Anzahl der Tasks im Project'
        return len(self.__tasks)

    def attr_dict(self):
        'Kopiert und ändert das self.__dict__ mit den Attributen der Klasse, so dass JSON damit klar kommt'
        'return'
        '  modifizierte Kopie des self.__dict__'

        # VORSICHT in python ist eine Zuweisung kein Kopieren eines Objectes in eine neue Instanz!
        odict = self.__dict__.copy()    # get attribute dictionary
        # print(odict)
        del odict["_Project__tasks"]    # remove reference to project
        
        l=list()
        for k, _t in self.__tasks.items() :
            l.append(_t._id)

        odict["tasks"]=l            
        # print (odict)
        return odict

    @classmethod
    def DeleteAllProjects(cls) :
        
        cls.__all_projects.clear()
        cls.__task_num=0


    @classmethod
    def WriteAllProjectsToJSON(cls,filehandle) -> str:
        'Schreibt alle Projects in eine Datei - Bereits doppeltes Schreiben in Dateien entfernt'
        'return'
        '   JSON String In der aktuellen Arbeitsversion '

        JSONstr=""
        out_dict=dict()

        for _id, _p in cls.__all_projects.items() :
            out_dict[_p._name]=_p.attr_dict()

        json.dump(out_dict, filehandle, sort_keys=True, indent=2)

        # TestCode, der wieder einliest und nochmal schreibt, um die Ergebnisse vergleichen zu können
        # jdict=json.loads(JSONstr)
        # with open('prj2.json', 'w') as f:
        #     json.dump(jdict, f, sort_keys=True, indent=2)

        JSONstr = json.dumps(out_dict, sort_keys=True, indent=2)
        return JSONstr

    @classmethod
    def ReadAllProjectsFromJSON(cls, filehandle) :
        'Liest Projekte aus einer JSON Datei ein und legt diese an'
        'return'
        '  Dictionary mit den neuen Projekten'

        jdict=dict()

        jdict=json.load(filehandle)

        new_prj=dict()

        for _id, _p in jdict.items() :
            np=Project(_p["_name"], _p["_emoij"], _p["_farbe"])
            new_prj[_p["_name"]]=np
            # print(f"{_p['_name']}: {np}")

            for tid in _p["tasks"] :
                _t=Task.FindTaskid(tid)
                # print(f"{tid} = {_t._name}")
                _t.SetProject(np)

        return new_prj

class Action:
    '''Definiert eine Aktion mit einem Startdatum
    VORSICHT: da __eq__ und __ne__ hier neu definiert sind und nur die Startzeit vergleichen
    funktioniert z.B. der Vergleich None != Action nicht!

    __eq__ __ne__ umgebaut und einen Test auf None vorgeschaltet
    '''

    def __init__(self, task : Task, zeit=datetime.datetime.now() ):
        'Neue Action erzeugen und in datetime seconds und microseconds auf 0 setzen'
        self._start=zeit.replace(second=0, microsecond=0)
        self._task=task
        self._id=task._id

    # https://docs.python.org/3.7/library/string.html#formatstrings
    # strftime("%m/%d/%Y, %H:%M:%S")

    def hms(self) -> str :
        'return'
        '  Uhrzeit der Action in der Form HH:MM:SS'
        return self._start.strftime("%H:%M:%S")
    
    def __str__(self):
        return "Action({} : {})". format(self._start.strftime("%Y-%m-%d %H:%M:%S"), self._task._name)

    # https://docs.python.org/3.3/reference/datamodel.html?highlight=__lt__#object.__lt__
    def __lt__(self, other ) :
        return self._start < other._start      

    def __le__(self, other ) :
        return self._start <= other._start      

    def __gt__(self, other ) :
        return self._start > other._start      

    def __ge__(self, other ) :
        return self._start >= other._start      

    def __eq__(self, other ) :
        if other == None:
            return False
        else:
            return self._start == other._start      

    def __ne__(self, other ) :
        if other == None:
            return True
        else:
            return self._start != other._start      


    # https://docs.python.org/3/library/datetime.html
    def __sub__(self, other ) :
        'Zeitdifferenz in Sekunden'

        td=(self._start - other._start)
#        return td.seconds  # So funktioniert das nicht, weil keine negative Zahlen entstehen und maximale Differenz ein Tag ist 
        return int(td.total_seconds())




class Calender:
    'Sammelt die Actions und verwaltet die Einträge und kann vermutlich auch zukünftig Berichte erstellen'


    def __init__(self,prefix="tt") :
        '''
        Init the calender

        attributes:
            private: 
                __acttions_list
                __notsorted
                __prefix
                __dirty
        '''
        self.__actions=list()
        self.__notsorted=False
        self.__prefix=prefix
        self.__dirty=False 

    def GetPrefix(self) -> str :
        return self.__prefix
        
        
    def append(self, act: Action) :
        """Eine Action anfügen ohne Prüfung z.B. auf Doppelte Einträge bzw. Einträge mit zu geringem Abstand
           Neuer Name analog list.append wegen Konsistenz
           Kein Test ob act != None -> das geht nämlich nicht!"""
        self.__actions.append(act)
        self.__notsorted=True
        self.__dirty=True 

    def add(self, act: Action) :
        """TODO to be discontinued"""
        self.append(act)

    def remove(self, act: Action) :
        'Eine Action aus der Liste der Aktionen entfernen'

        self.__actions.remove(act)
        self.__dirty=True

    def removeAtTime(self, time: datetime) :
        'Die Action zu einer bestimmten Zeit aus der Liste der Aktionen entfernen'
        act=self.findExact(time)
        self.__actions.remove(act)
        self.__dirty=True

    def removeIDAtTime(self, id_, time: datetime) -> Task:
        ''' Finde genau die Action, mit genau der Uhrzeit und lösche sie
         return:
             die gefundene Action'''

        time=time.replace(second=0, microsecond=0)

        if self.__notsorted :
            self.sort()

        for i in range(len(self.__actions)-1,0,-1) :
            if self.__actions[i]._start < time :
                break
            if self.__actions[i]._start == time :
#                if self.__actions[i]._task._id == id_ :
                if self.__actions[i]._id== id_ :
                    self.__actions.remove(self.__actions[i])
                    self.__dirty=True
                    return self.__actions[i]
        'Wenn die Schleife komplett durchläuft dann wurde nichts gefunden'

        return None


    def removeBetween(self, fro: datetime, til:datetime) -> int :
        """Die Action zwischen zwei Zeitpunkten o <= action < o aus der Liste der Aktionen entfernen
            Benutzt findBetween
            return
                Anzahl der gelöschten Objekte"""

        fcal=self.findBetween(fro,til)
        i=0
        for _a in fcal.__actions :
            self.__actions.remove(_a)
            self.__dirty=True
            i=i+1
            
        return i


    def __str__(self) :
        s= "Calender(\n"
        for a in self.__actions:
            s +=  "  {0}\n".format(a)
        return s + ")"

    def len(self) -> int:
        'return'
        '  Anzahl der Actions im Calender'
        return len(self.__actions)

    def sort(self):
        'sortiere die Liste der Actions nach _start (=Zeit)'

        self.__actions.sort()            
        self.__notsorted=False

    def findExact(self, time: datetime) :
        ''' Finde den ersten Eintrag, die erste Action, mit genau der Uhrzeit / oder besser Zeitdifferenz <= 1 Sekunde?
         return:
             die gefundene Action'''

        if self.__notsorted :
            self.sort()
        for id in range(len(self.__actions)-1,0,-1) :
            if self.__actions[id]._start < time :
                break
            if self.__actions[id]._start == time :
                return self.__actions[id]
        'Wenn die Schleife komplett durchläuft dann wurde nichts gefunden'
        return None # TODO wäre RÜckgabe von 0 im Fehlerfall besser? 

    def findFuzzy(self, time: datetime, seconds_diff=10*60) :
        'Sammle Actions mit ungefähr der Uhrzeit d.h. Abstand < Parameter seconds_diff '
        ' return:'
        '     Neues Calender Objekt mit den gefundenen Actions, reverse order'
        td = timedelta(weeks=0, days=0, hours=0, minutes=0, seconds=seconds_diff)

        print ("** FindeFuzzy {} {}={}".format(time,seconds_diff,td))
        print ("** {} bis {}".format(time-td, time+td))
        # print ("** ",list(range(len(self.__actions)-1,0,-1)),"\n")


        if self.__notsorted :
            self.sort()

        foundCal=Calender()


        for id in range(len(self.__actions)-1,0,-1) :
            # print ("   {}= {} diff = {}".format(id,self.__actions[id],self.__actions[id]._start-time))
            if self.__actions[id]._start < (time - td):
                break
            if self.__actions[id]._start < (time + td):
                foundCal.add(self.__actions[id])

        return foundCal

    def findBetween(self, start: datetime, end: datetime) :
        'Sammle Actions mit self._start >= start und self._start < end'
        'Könnte auch als Implementierung von fuzzy dienen'
        ' return:'
        '     Neues Calender Objekt mit den gefundenen Actions, NON reverse order'

        # print ("** FindeBetween {} bis {}".format(start,end))

        if self.__notsorted :
            self.sort()

        foundCal=Calender()


        for id in range(len(self.__actions)-1,0,-1) :
            # print ("   {}= {} diff = {}".format(id,self.__actions[id],self.__actions[id]._start-start))
            if self.__actions[id]._start < start:
                break
            if self.__actions[id]._start < end:
                foundCal.add(self.__actions[id])

        foundCal.sort()
        return foundCal

    def findTask(self, search_task ) :
        'Sammle Actions mit dieser Task, anhand Task._id'
        ' return:'
        '     Neues Calender Objekt mit den gefundenen Actions, NON reverse order'

        # print ("** findTask {} ".format(search_task._name))

        if self.__notsorted :
            self.sort()

        foundCal=Calender()


        for id in range(0,len(self.__actions)-1) :
            if self.__actions[id]._id == search_task._id:
                foundCal.add(self.__actions[id])

        foundCal.sort()
        return foundCal

    def CalcDurations(self) -> dict :
        """ Zeiten in einem kompletten Kalenderobject je Task sammeln, addieren und auf Minuten runden
            return
                Dictionary mit Task._id als Index und als Wert eine Liste Minuten, Task._name, Task._projektName
        """

        if self.__notsorted :
            self.sort()

        minu=dict()

        l = len(self.__actions)
        for index in range(0,len(self.__actions)-1) :
            _a=self.__actions[index]
            td = self.__actions[index+1]._start - _a._start


            # print(f"*** {index} von {l} : {self.__actions[index]._task._name} = {td} = {round(td.total_seconds()/60)}")

            if _a._id in minu :
                # print(f"{index}: aufaddieren {minu[_a._id]} t={minu[_a._id][0]}")
                t= minu[_a._id][0] + round(td.total_seconds()/60)
                h= round(t/60*10)/10
                minu[_a._id]= (t, h, _a._task._name, _a._task._projectName)
            
            else :
                t=round(td.total_seconds()/60)
                minu[_a._id]= (t, round(t/60*10)/10, _a._task._name, _a._task._projectName)
                # print(f"{index}: neu erzeugt: {minu[_a._id]}")
        if 0 in minu:
            del minu[0]
        return minu


    def WriteDurationsToCSV(self, filehandle):

        erg = self.CalcDurations();

        # how can i sort this dict with values, that are lists?        
    
        spamwriter = csv.writer(filehandle,delimiter=";")
        # Durch dict iterieren und den Wert = Liste mit TaskName und Minuten in csv schreiben
        spamwriter.writerow(("Minutes","Hours","Task","Project"))
        for k, v in erg.items():
            spamwriter.writerow(v)


    def UICalcDurations(self) -> list :
        """Addding times for actions in this calender and
        build a list of dict, that fits the needs of the Pythonista UI
        """

        dl=self.CalcDurations()

        l=list()
        for k,v in dl.items() :
            if k != "Date" and k!= "0" and k !=0 :
                l.append({"title":f"{v[2]}", 'hour':round(v[0]/6)/10, 
                'prj':f"{v[3]}" })
#        l =sorted(l, key = lambda i: (i['prj']))

        # negative Stundenzahl als Sortierkriterium
        l =sorted(l, key = lambda i: (i['prj'], -i['hour']))
#       l= sorted(l, key = lambda i: (i['prj'], i['name'])) 

        # https://www.geeksforgeeks.org/ways-sort-list-dictionaries-values-python-using-itemgetter/
        return l

    def MonthReport(self, date: datetime)  -> dict :      
        """ Erstellt einen Monatsreport für den Monat, der in <date> angegeben wird
            Sollte ich an geeigneter Stelle auch den Monat integrieren in das dict?
            Ginge ja
            return
                dict with tasks and their monthly duration in minutes
        """
            
        mstart=date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        mend=mstart+timedelta(weeks=0, days=32, hours=0, minutes=0, seconds=0)  
        mend=mend.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        # print(f"\n\*** MonthReport({date})")
        # print(f"    Monatsstart = {mstart}")
        # print(f"    +1Monat     = {mend}")

        mcal=self.findBetween(mstart,mend)
        d=mcal.CalcDurations()

        d["Date"]=(date, mstart, mend)
        return d

    def SaveAndRemoveMonth(self, date: datetime, path:str)  :      
        """ Speichert die Actions für den Monat, der in <date> angegeben wird in einem CSV
            und löscht diese dann aus dem Calender >> NOCH NICHT IMPLEMENTIERT <<
            return
                ?
        """
            
        mstart=date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        mend=mstart+timedelta(weeks=0, days=32, hours=0, minutes=0, seconds=0)  
        mend=mend.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        print(f"\n\*** SaveAndRemoveMonth({date} to {path})")
        print(f"    Monatsstart = {mstart}")
        # print(f"    +1Monat     = {mend}")

        mcal=self.findBetween(mstart,mend)

        fname =path+mstart.strftime("%Y_%m")+ "_TiTraCal.csv"
        print(f"    Filename = {fname}")


        with open(fname, 'w', newline='') as f:
            w=mcal.WriteCalToCSV(f)

        print(f"    written = {w}")            

        self.removeBetween(mstart,mend)   # TODO kontrollieren, ob diese Routine auch die selben Regeln auswertet wie find ...
        return w

    def listActionsOfToday(self) -> list :
        now=datetime.datetime.now()
        return self.listActionsOfDay(now)

    def listActionsOfDay(self, day:datetime) -> list :
        
        dstart=day.replace(hour=0, minute=0, second=0, microsecond=0)
        dend=dstart+timedelta(days=1)

        dcal=self.findBetween(dstart,dend)

        dlist=list()
        for a in dcal.__actions:
            td = (a._start - dstart)
            mi= round(td.total_seconds()/60)
            dlist.append((mi, a._task._farbe ,a._start.strftime("%H:%M"), a._task._name, a._task._projectName,a._start.strftime("%Y-%m-%d")))

        return dlist

    def UIActionsOfDayList(self, day:datetime) -> list :
        
        dstart=day.replace(hour=0, minute=0, second=0, microsecond=0)
        dend=dstart+timedelta(days=1)

        dcal=self.findBetween(dstart,dend)

        dlist=list()
        for a in dcal.__actions:
            td = (a._start - dstart)
            mi= round(td.total_seconds()/60)
#            dlist.append((mi, a._task._farbe ,a._start.strftime("%H:%M"), a._task._name, a._task._projectName,a._start.strftime("%Y-%m-%d")))
            d={'long':f"{a._start.strftime('%H:%M')} {a._task._name} [{a._task._projectName}]",
               'task':a._task._name,
               'prj': a._task._projectName,
               'id': a._task._id,
               'color': a._task._farbe,
               'minute': mi,
               'time':a._start.strftime('%H:%M'),
               'date':a._start.strftime('%Y-%m-%d')}

            # print(d)
            dlist.append(d)

        return dlist


    def StartActionName(self,name,time) :
        'Neue Action anhand Name in Calender einfügen'
        'return'
        '  neu angelegt Action bzw. None'
        _t=Task.FindTaskName(name)

        if None != _t:
            _a = _t.NewAction(time)
            self.add(_a)
            return(_a)

        return(None)

    def StartActionNameTodayHM(self,name,hm) :
        'Neue Action anhand Name in Calender für heute mit Uhrzeit HH:MM einfügen'
        'return'
        '  neu angelegt Action bzw. None'

        _t=Task.FindTaskName(name)

        if None != _t:
            time=datetime.datetime.now()
            regex = r"([0-2]?\d):([0-6]\d)"

            m=re.match(regex,hm)    

            if m :
                # print (m.groups())
                # print (m.group(0))
                # print (m.group(1))
                # print (m.group(2))
                
                time=time.replace(hour=int(m.group(1)),minute=int(m.group(2)),second=0,microsecond=0)            
                _a=_t.NewAction(time)
                self.add(_a)
                return (_a)
        return(None)

    def SaveCal(self) -> int :
        '''Save the Calender Data to CSV
            filename <prefix>.cal.csv

            check if __dirty
            check if file exists, then copy to *bak.csv
        '''

        if self.__dirty :
            if os.path.exists(self.__prefix +".cal.csv"):
                shutil.copy2(self.__prefix +".cal.csv",self.__prefix +".cal.bak.csv")        
            with open(self.__prefix +".cal.csv", "w" ) as f:
                i=self.WriteCalToCSV(f)
                self.__dirty=False
                return i

    def WriteCalToCSV(self,filehandle) -> int :
        """Schreibt den Calender d.h. alle Action Einträge als csv Datei raus
            return
               Anzahl der geschriebenen Sätze"""

        if self.__notsorted :
            self.sort()

        writer = csv.writer(filehandle,delimiter=";",quoting=csv.QUOTE_NONNUMERIC)
        writer.writerow(("Zeit", "Name", "Projekt", "ID"))

        written=0

#        for index in range(0,len(self.__actions)-1) :
#            _a=self.__actions[index]
        for _a in self.__actions :
            writer.writerow((_a._start, _a._task._name, _a._task._projectName, _a._task._id))
            written +=1

        return written

    def LoadCal(self):
        with open(self.__prefix +".cal.csv", "r" ) as f:
            self.ReadCalFromCSV(f)


    def ReadCalFromCSV(self,filehandle):
        'Liest einen Calender aus einem CSV d.h. alle Action Einträge werden neu angelegt'
        'Voraussetzung ist, dass die entsprechenden Tasks schon vorhanden sind!'

        # https://realpython.com/python-csv/
        # https://docs.python.org/3/library/csv.html

        reader = csv.DictReader(filehandle,delimiter=";",quoting=csv.QUOTE_NONNUMERIC)
        try:
            for row in reader:
                # print(row)
                _t=Task.FindTaskid(int(row['ID']))
                dt=datetime.datetime.strptime(row['Zeit'],"%Y-%m-%d %H:%M:%S")
                _a=_t.NewAction(dt)

                'if _a != None : # ?? Testen ob Task wirklich gefunden wurde '
                
                self.add(_a)

        except csv.Error as e:
            print('file {}, line {}: {}'.format(filehandle, reader.line_num, e))
            exit(1)



    def SaveTasks(self) -> int :
        '''Save the tasks data to json
            filename <prefix>.tasks.json

            check if file exists, then copy to *bak.json
        '''

        if True :
            if os.path.exists(self.__prefix +".tasks.json"):
                shutil.copy2(self.__prefix +".tasks.json",self.__prefix +".tasks.bak.json")        
            with open(self.__prefix +".tasks.json", "w" ) as f:
                return len(Task.WriteAllTasksToJSON(f))

    def LoadTasks(self) -> int :
        '''Load the tasks data from json
            filename <prefix>.tasks.json
        '''
        with open(self.__prefix +".tasks.json", 'r') as f:
            at=Task.ReadAllTasksFromJSON(f)
            return len(at)

    def SaveProjects(self) -> int :
        '''Save the tasks data to json
            filename <prefix>.prj.json

            check if file exists, then copy to *bak.csv
        '''

        if True :
            if os.path.exists(self.__prefix +".prj.json"):
                shutil.copy2(self.__prefix +".prj.json",self.__prefix +".prj.bak.json")        
            with open(self.__prefix +".prj.json", "w" ) as f:
                return len(Project.WriteAllProjectsToJSON(f))

    def LoadProjects(self) -> int:            
        '''Load the projects data from json
            filename <prefix>.tasks.json
        '''            
        with open(self.__prefix +".prj.json", 'r') as f:
            ap=Project.ReadAllProjectsFromJSON(f)
            return len(ap)






def InitTaskProjects(deb):
    nullprj=Project("Null","-","#004400")
    stopper=Task("stopper","-","#004400")
    stopper.SetProject(nullprj)

    stdprj=Project("Standard","x", "#AAAAAA")
    atask=Task("BL","x","#AAAAAA")
    atask.SetProject(stdprj)

    atask=Task("Risikocontrolling","x","#AAAAAA")
    atask.SetProject(stdprj)

    atask=Task("NZU","x","#AAAAAA")
    atask.SetProject(stdprj)

    atask=Task("FABank","!","#AA8800")
    atask.SetProject(stdprj)

    atask=Task("AG Risiko","!","#AA8800")
    atask.SetProject(stdprj)

    atask=Task("Revision.Vorb","!","#662200")
    atask.SetProject(stdprj)

    atask=Task("Revision.Nachb","!","#662200")
    atask.SetProject(stdprj)

    _44prj=Project("44er Projekt","O", "#6060FF")
    atask=Task("44.PJL","o","#6060FF")
    atask.SetProject(_44prj)

    atask=Task("Ablauffiktion","o","#6060FF")
    atask.SetProject(_44prj)

    MZBprj=Project("MZB","O", "#60FFFF")
    atask=Task("MZB.PJL","o","#60FFFF")
    atask.SetProject(MZBprj)

    atask=Task("MZB.Ablauffiktion","o","#60FFFF")
    atask.SetProject(MZBprj)

    print(f"\n>>> WriteAll Tasks & Projects toJSON\n")

    with open('tasks.json', 'w') as f:
        Task.WriteAllTasksToJSON(f)
    with open('prj.json', 'w') as f:
        Project.WriteAllProjectsToJSON(f)


def ReadTasksProjects() :
    with open('tasks.json', 'r') as f:
        Task.ReadAllTasksFromJSON(f)
    with open('prj.json', 'r') as f:
        Project.ReadAllProjectsFromJSON(f)


