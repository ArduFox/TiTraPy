# coding: utf-8
#
# TiTraPy.py
#
# part of TiTraPy = TimeTracker for pythonistas
# contains code for UI and initialization
# uses pythonista specific libraries especially for GUI in iOS
#
# 
# Changes in V 00.81
# - new custom view with class shows diagram of hours in week
#
#
#
# ===== Release V 00.80 ==================================================== 
#
# Changes in V 00.80
# - when selecting action in cal_view time is set to that of selected action
#
# Changes in V 00.77
# - Better handling of errors in reading tasks, projects and calenders - not 
#   finished yet: handle tasks without projects!
# - added GPL Licence
# - eliminated debugging prints
# - added adaptive column chart of actions of day with labels of time and task
# - problems when writing german umlauts solved by adding 
#   encoding='utf8',errors="ignore" to open file
#   Why is this only appearing in CSV and not on JSON?
#
# Changes in V 00.76
# - console.hud used to show success at saving calender & hours.csv. 
#   NOTE: console.hide_activity dismisses the hud. 
#         return of hud dont resets activity indicator
#
# Changes in V 00.75
# - saved *.csv of durations contains now hours
# - code reformatted PEP8 and cleaned
# - fixed stupid error in TiTra.Calender.removeIDAtTime, when deleting very 
#   last item in Calender.
#
# Changes in V 00.74
# - Cleaing Up UI and showing some elements only if prefix in ("test", "DEV")
# - Button Save is aware of information shown in panel / tableview and changes 
#   title and saves appropriate data
#
# Changes in V 00.73
# - using the new Calender methods for reading and saving tasks, projects, calender
# - at the end of the file, the Calender instance will be set to prefix DEV. 
#   All saved files will therfore start with DEV.
# - coded sharing of hours .csv
# - in TiTra.py Calender calculate hours and sort Output of CalcDurations
# - enabling / disabling buttons and hiding labels depending whats to see in 
#   right / second tableview
#
# Changes in V 00.72
# - using now a segemented control to change view in second pane
# - remaining code of VersionInStatusbar eliminated
# - Using custom view for main view to trap will_change() for saving the 
#   calender just before app exits
# - cleaning up the ui
# - added controls for saving and mailing calculated hours per day/week/month
# - added stubble of code to realy save the hours
# 
# Changes in V 00.71
# - added class variable myCalender in ShowTView, to contain the instance of 
#   TiTra.Calender
# - load TiTraPy.pyui
#
# 
#
#
# -----------------------------------------------------------------------------
#    Licence & Copyright
# -----------------------------------------------------------------------------
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



import console, os, ui
import datetime
from datetime import timedelta
#from datetime import date

import random
#import json
#import re
#import csv
#import os
import sys
import shutil

import TiTra
import DataSources as MDS

version = '00.81'

# for get_available_memory
from ctypes import *
from objc_util import ObjCClass

#import ui


class MyView(ui.View):
  '''from pythonista ui documentation
       I need it to implement will_close() to save the data when ui is exited
       
       Lessons learned
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
    self.cal = None
    pass

  def setCalender(self, cal: TiTra.Calender):

    self.cal = cal

  def did_load(self):
    # This will be called when a view has been fully loaded from a UI file.
    pass

  def will_close(self):
    # This will be called when a presented view is about to be dismissed.
    # You might want to save data here.

    # print("My_View.will_close saving Calender at ",
    #      datetime.datetime.now().strftime("%H:%M:%S"))
    if None != self.cal:
      console.show_activity()
      cal.SaveCal()
      self.CalChanged = False
      console.hud_alert("calender saved", 'success')
      #            print("Calender gespeichert: cal.csv")
      console.hide_activity()

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


import ui


class BoxPlotView(ui.View):
  def __init__(self):
    # This will also be called without arguments when the view is loaded from a UI file.
    # You don't have to call super. Note that this is called *before* the attributes
    # defined in the UI file are set. Implement `did_load` to customize a view after
    # it's been fully loaded from a UI file.
    self._actions = list()
    day = datetime.datetime.today()
    dnull = day.replace(hour=0, minute=0, second=0, microsecond=0)
    dstart = day.replace(hour=8, minute=30, second=0, microsecond=0)
    dend = day.replace(hour=19, minute=30, second=0, microsecond=0)

    td = dstart - dnull
    self._minu_start = round(td.total_seconds() / 60)
    td = dend - dstart
    self._minu_len = round(td.total_seconds() / 60)

  def did_load(self):
    # This will be called when a view has been fully loaded from a UI file.
    #        self._divisor= self._minu_len / ( self.height -30)

    #        print (f"BoxPlot minu_len {self._minu_len} height {self.height} divisor {self._divisor:5.3f}")      
    pass

  def will_close(self):
    # This will be called when a presented view is about to be dismissed.
    # You might want to save data here.
    pass

  def SetActions(self, acts: list):
    self._actions.clear()
    self._actions = acts

    mstart = 24 * 60 * 2
    mend = 0
    for ta in self._actions:
      mstart = min(ta["minute"], mstart)
      mend = max(ta["minute"], mend)

#        self._minu_len=max(self._minu_len,(mend-mstart)) # throughout usage _minu_len only gets more
    self._minu_len = (mend - mstart)
    self._divisor = self._minu_len / (self.height - 40)

    #        print (f"BoxPlot minu_len {self._minu_len} end-start {(mend-mstart)} height {self.height} divisor {self._divisor:5.3f}")      
    self.set_needs_display()

  def draw(self):
    # This will be called whenever the view's content needs to be drawn.
    # You can use any of the ui module's drawing functions here to render
    # content into the view's visible rectangle.
    # Do not call this method directly, instead, if you need your view
    # to redraw its content, call set_needs_display().

    if len(self._actions) < 2:
      return

    y = 10
    mi_start = 0

    # pseudo code
    #
    # get first entry
    #   set start & y at .minute
    #   know name & color & starttime
    # while next entry
    #   len = this.minute - start
    #   draw previous name, color, len, starttime

    i = 0
    for ta in self._actions:
      _t = TiTra.Task.FindTaskid(int(ta["id"]))
      i += 1

      if mi_start != 0:
        h = float(ta["minute"] - mi_start) / self._divisor

        ui.fill_rect(30, y, 20, h)
        ui.draw_string(time_str, rect=(2, y - 5, 0, 0), font=('<system>', 10))
        #            ui.draw_string(str(h),        rect=(52,y-5,0,0),font=('<system>', 7))
        #            ui.draw_string(str(round(y)), rect=(5,y+10,0,0),font=('<system>', 7))
        #            ui.draw_string(str(ta["minute"]), rect=(52,y-5,0,0),font=('<system>', 7))
        ui.draw_string(
          name_str, rect=(52, y + h / 3, 0, 0), font=('<system>', 9))
        y = y + h + 2

      #_t=TiTra.Task.FindTaskid(i)
      #          _t=TiTra.Task.FindTaskid(random.randint(0,13))

      ui.set_color(_t._farbe)
      time_str = ta["time"]
      name_str = _t._name
      mi_start = ta["minute"]

      if i == len(self._actions):
        ui.draw_string(
          ta["time"], rect=(0, y - 5, 0, 0), font=('<system>', 10))

      # if this is last entry of the day
      # this will not be drawn, but the time should be 
      # displayed
      #
      # normaly this is id==0
      # but during the day maybe this is also a not completed task

      # ui.fill_rect(x, y, width, height)
      # Fill the given rect with the current color (set via set_color()).

      # ui.set_color(color)
      # Set the current drawing color. This has an effect on following drawing operations, e.g. fill_rect() or Path.fill().

      # ui.draw_string(string, rect=(0, 0, 0, 0), font=('<system>', 12), color='black', 
      #                alignment=ui.ALIGN_LEFT, line_break_mode=ui.LB_WORD_WRAP)
      # Draw a string into the given rectangle. If the rectangle’s size is zero, 
      # the drawing will use its origin as the drawing position, but the size will be unconstrained.

  def keyboard_frame_will_change(self, frame):
    # Called when the on-screen keyboard appears/disappears
    # Note: The frame is in screen coordinates.
    pass

  def keyboard_frame_did_change(self, frame):
    # Called when the on-screen keyboard appears/disappears
    # Note: The frame is in screen coordinates.
    pass


class BoxAreaPlotView(ui.View):
  '''Draws a rectangular altenative to an pie chart
       in which each area is as big as its share of the total area
       Needs a CustomView Element in the .pyui
       
       Based on BoxPlotView from TiTraPy.py
    '''

  def __init__(self):
    ''' This will also be called without arguments when the view is loaded from a UI file.
          You don't have to call super. Note that this is called *before* the attributes
          defined in the UI file are set. Implement `did_load` to customize a view after
          it's been fully loaded from a UI file.
        '''

    self._actions = list()
    day = datetime.datetime.today()
    dnull = day.replace(hour=0, minute=0, second=0, microsecond=0)
    dstart = day.replace(hour=8, minute=30, second=0, microsecond=0)
    dend = day.replace(hour=19, minute=30, second=0, microsecond=0)

    td = dstart - dnull
    self._minu_start = round(td.total_seconds() / 60)
    td = dend - dstart
    self._minu_len = round(td.total_seconds() / 60)

    self.totalArea = self.height * self.width
    self.LeftHeight = self.height
    self.LeftWidth = self.width

  def did_load(self):
    ''' This will be called when a view has been fully loaded from a UI file. '''
    pass

  def will_close(self):
    # This will be called when a presented view is about to be dismissed.
    # You might want to save data here.
    pass

  def SetActions(self, acts: list):
    '''Update Actions and meassurements in member variables needed to 
           draw the plot
         
           what form does the list act have?
           - list of dicts
           - each entry has at least a key "minute", "time", "id"
        '''

    self._actions.clear()
    self._actions = acts

    self.LeftHeight = self.height
    self.LeftWidth = self.width

#    print("\nactions in BoxAreaPlot ", self._actions)

    self.set_needs_display()

  def draw(self):
    ''' This will be called whenever the view's content needs to be drawn.
            You can use any of the ui module's drawing functions here to render
            content into the view's visible rectangle.
            Do not call this method directly, instead, if you need your view
            to redraw its content, call set_needs_display().
        '''

    #TODO doesnt draw in a spiral with smallest in the center - just alternate to right / to bottom
    
    if len(self._actions) < 2:
      return

    y = 0
    x = 0
    vertical = True

    i = 0

    # iterate self._actions[:-1]
    # means we do it not for last one
    # then execute the code in loop only for last one

    for ta in self._actions:
      _t = TiTra.Task.FindTaskName(ta["title"])
      ui.set_color(_t._farbe)

      hell = sum(ui.parse_color(_t._farbe)[0:3])

      text_col = "black"

      if hell < 3 * 0.67:
        text_col = "white"

      i += 1

#      print(f"\n{i}: {ta['title']} = {ta['percent']:4.2} % = {ta['area']}")
#      print("farbe=", _t._farbe, ui.parse_color(_t._farbe), hell)
#      print(
#        f"Left w/h ({self.LeftWidth}/{self.LeftHeight}) x/y = ({x}/{y}) vertical = {vertical}"
#      )

      if vertical:

        if self.LeftWidth == 0:
          print("LeftWidth==0 return >> ")
          return

        y2 = round(ta["area"] / self.LeftWidth)

        ui.fill_rect(x, y, self.LeftWidth - 1, y2 - 1)
#        ui.draw_string(str(y2), rect=(x, y + 2, 0, 0), font=('<system>', 6))
        ui.draw_string(
          str(ta["hour"]) + "h",
          rect=(x + self.LeftWidth / 2-8, y + 2, 0, 0),
          font=('<system>', 7),
          color=text_col)
        ui.draw_string(
          ta['title'],
          rect=(x + 3, y + y2 / 2-4, 0, 0),
          font=('<system>', 8),
          color=text_col)

#        print(f"x/y2 ({x}/{y2}) rect xywh ({x}/{y}, {self.LeftWidth}/{y2})")

        self.LeftHeight -= y2
        y += y2
        vertical = False

      else:
        if self.LeftHeight == 0:
          print("LeftHeight==0 return >> ")
          return

        x2 = round(ta["area"] / self.LeftHeight)

        ui.fill_rect(x, y, x2 - 1, self.LeftHeight - 1)
#        ui.draw_string(str(x2), rect=(x + 2, y, 0, 0), font=('<system>', 6))
        ui.draw_string(
          str(ta["hour"]) + "h",
          rect=(x + x2 / 2-8, y + 2, 0, 0),
          font=('<system>', 7),
          color=text_col)
        #print(str(ta["hour"]) + "h",ui.measure_string(str(ta["hour"]) + "h",  font=('<system>', 7)))
        ui.draw_string(
          ta['title'],
          rect=(x + 3, y + self.LeftHeight / 2-4, 0, 0),
          font=('<system>', 8),
          color=text_col)

#        print(f"x2/y ({x2}/{y})  rect xywh ({x}/{y}, {x2}/{self.LeftHeight})")

        self.LeftWidth -= x2
        x += x2
        vertical = True


class ShowTableView(object):
  def __init__(self, cal: TiTra.Calender):
    '''init UI, load pyui file
           keeps a list of messages for LogMessage(line:str) 

           self.selected_row
           self.state        which view is activ? whats the content of the second / right tableview
        '''
    self.view = ui.load_view('TiTraPy.pyui')
    self.labelcounter = 0
    self.msglist = list()
    self.ui_lmsg = self.view['l_msg']
    self.state = 0
    self.selected_row = -1
    self.selected = None
    self.myCalender = cal
    self.CalChanged = False

    self.view.setCalender(self.myCalender)

    self.view.present('fullscreen')

    root, ext = os.path.splitext(sys.argv[0])  # script path without .py
    script_name = os.path.basename(root)  # script name without the path
    self.LogMessage(script_name)

    listOfDirs = root.split('/')
    l = len(listOfDirs) - 1
    pre = self.myCalender.GetPrefix()
    if pre in ("DEV"):
      pass
    else:
      self.view["bt_BackupMonth"].hidden = True
      self.view["bt_save_all"].hidden = True
      self.view["bt_CopyPy"].hidden = True
      self.view["l_msg"].hidden = True
      #self.view["BoxPlotView"].hidden=True

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
    tv1.row_height = 26

    tv2 = self.view['tableview2']
    tv2.row_height = 26

    # (font_name, font_size). In addition to regular font names, you can also use ('<system>',14) or '<system-bold>'

    # Button.font
    # The font for the button’s title as a tuple (font_name, font_size). In addition to regular font names, you can also
    # use '<system>' or '<system-bold>' to get the default regular or bold font.
    now = self.view['datepicker'].date
    self.view["BoxPlotView"].SetActions(
      self.myCalender.UIActionsOfDayList(now))
    self.GetBoxAreaData(None)

    self.bt_task_action(None)
    self.bt_cal2_action(None)
    self.LogMessage("init done.")

  def LogMessage(self, line: str):
    '''log a message to MessageBoard to show the user / developer what happend
        '''

    #print(f"Listenlänge {len(self.msglist)}. Textlänge {len(self.ui_lmsg.text)}")
    if len(self.msglist) > 7:
      # or len(self.ui_lmsg.text) > 100:
      # print("pop msglist")
      self.msglist.pop(0)

      # pop löscht das letzte Element

    nowstr = datetime.datetime.today().strftime("%H:%M:%S : ")
    self.msglist.append(nowstr + line)
    self.ui_lmsg.text = "\n".join(self.msglist)

  def bt_empty_action(self, sender):
    '''clear tableview1
        '''
    tv1 = self.view['tableview1']
    tv1.data_source = tv1.delegate = ui.ListDataSource([])
    tv1.data_source.delete_enabled = tv1.editing = False
    tv1.reload_data()
    self.view['bt_save_hours'].enabled = False
    self.view['bt_add'].enabled = False

  def bt_task_action(self, sender):
    ''' fill "tableview1" with List of Tasks
        '''
    lst = MDS.MyTaskDataSource(TiTra.Task.UITasksList())
    #print(f"\nShow tasks {TiTra.Task.UITasksList()}")
    tv1 = self.view['tableview1']
    tv1.data_source = tv1.delegate = lst
    tv1.data_source.delete_enabled = tv1.editing = False
    lst.action = self.tv_task_action
    self.state = 1
    self.selected_row = -1
    tv1.reload_data()
    #        tv1.font=('<system>',12)
    self.view['bt_add'].enabled = True
    #        self.view['bt_save_hours'].enabled=False
    self.view['bt_save_hours'].title = "Save Cal"
    self.view['label_up'].hidden = False
    self.view['label_left'].hidden = False
    self.view['switch_share_hours'].hidden = True
    self.view['l_share'].hidden = True

    self.get_available_memory()

  def bt_cal2_action(self, sender):
    ''' fill "tableview2" with list of calender entries = actions
        '''
    now = self.view['datepicker'].date
    # datetime.datetime.today()

    lst = MDS.MyCalDataSource(self.myCalender,
                              self.myCalender.UIActionsOfDayList(now))
    tv2 = self.view['tableview2']
    tv2.data_source = tv2.delegate = lst
    tv2.data_source.delete_enabled = tv2.editing = False
    lst.action = self.tv_cal_action
    #        self.state=2
    #        self.selected_row=-1
    tv2.reload_data()
    self.get_available_memory()

  def bt_dur_day_action(self, sender):
    ''' fill "tableview1" with list of duration of tasks in selcted day
        Anzeigen welche Zeiten für welche Tasks gebraucht wurden
        '''
    start = self.view["datepicker"].date

    start = start.replace(hour=0, minute=0, second=0, microsecond=0)
    end = start + timedelta(days=1)

    lc = self.myCalender.findBetween(start, end)
    l = lc.UICalcDurations()

    self.LogMessage(f"dur_day_action len {len(l)}")

    #self.LogMessage(f"dur_day_action liste {len(l)}")    
    lst = MDS.MyDurDataSource("daily", l)
    lst.highlight_color = (1.0, 0.9, 0.3, 1.0)
    tv1 = self.view['tableview1']
    tv1.data_source = tv1.delegate = lst
    tv1.data_source.delete_enabled = tv1.editing = False
    self.selected_row = -1
    tv1.reload_data()
    self.view['bt_save_hours'].enabled = True
    if self.state == 1:
      self.view['bt_save_hours'].title = "Save Hours"
      self.view['switch_share_hours'].hidden = False
      self.view['l_share'].hidden = False
      self.view['bt_add'].enabled = False
      self.view['label_up'].hidden = True
      self.view['label_left'].hidden = True
    self.state = 3

  def bt_dur_week_action(self, sender):
    ''' fill "tableview1" with list of duration of tasks in the week, the selected day is in
        '''
    start = self.view["datepicker"].date
    start = start.replace(hour=0, minute=0, second=0, microsecond=0)
    monday = start - timedelta(days=start.weekday())
    satday = monday + timedelta(days=5)

    lc = self.myCalender.findBetween(monday, satday)
    l = lc.UICalcDurations()

    self.LogMessage(
      f"dur_week_action len {len(l)} {monday.strftime('%a %d.%m.%y')}")

    #self.LogMessage(f"dur_day_action liste {len(l)}")    
    lst = MDS.MyDurDataSource("weekly", l)
    lst.highlight_color = (1.0, 0.9, 0.3, 1.0)
    tv1 = self.view['tableview1']
    tv1.data_source = tv1.delegate = lst
    tv1.data_source.delete_enabled = tv1.editing = False
    self.selected_row = -1
    tv1.reload_data()
    self.view['bt_save_hours'].enabled = True
    if self.state == 1:
      self.view['bt_save_hours'].title = "Save Hours"
      self.view['switch_share_hours'].hidden = False
      self.view['l_share'].hidden = False
      self.view['bt_add'].enabled = False
      self.view['label_up'].hidden = True
      self.view['label_left'].hidden = True
    self.state = 4

  def bt_dur_month_action(self, sender):
    ''' fill "tableview1" with list of duration of tasks in the month, the selected day is in
        '''
    start = self.view["datepicker"].date
    #        self.view["datepicker"].font=("<system>",12). # WHAT is THIS ??

    mstart = start.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    mend = mstart + timedelta(weeks=0, days=32, hours=0, minutes=0, seconds=0)
    mend = mend.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    lc = self.myCalender.findBetween(mstart, mend)
    l = lc.UICalcDurations()

    self.LogMessage(f"dur_month_action len {len(l)}")
    lst = MDS.MyDurDataSource("monthly", l)

    #lst.font=("<system>",12)
    lst.highlight_color = (1.0, 0.9, 0.3, 1.0)
    tv1 = self.view['tableview1']
    tv1.data_source = tv1.delegate = lst
    tv1.data_source.delete_enabled = tv1.editing = False
    self.selected_row = -1
    tv1.reload_data()
    self.view['bt_save_hours'].enabled = True
    if self.state == 1:
      self.view['bt_save_hours'].title = "Save Hours"
      self.view['switch_share_hours'].hidden = False
      self.view['l_share'].hidden = False
      self.view['bt_add'].enabled = False
      self.view['label_up'].hidden = True
      self.view['label_left'].hidden = True
    self.state = 5

  def bt_save_hours_action(self, sender):
    '''save the content of the actual view of hours per day/week/month to csv.file
        '''
    #console.show_activity()
    start = self.view["datepicker"].date

    if self.state == 5:  # month
      mstart = start.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
      mend = mstart + timedelta(
        weeks=0, days=32, hours=0, minutes=0, seconds=0)
      mend = mend.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

      lc = self.myCalender.findBetween(mstart, mend)
      self.LogMessage(f"save week of {mstart.strftime('%a %d.%m.%y')}")
      fname = f"{mstart.strftime('%y-%m-%d')}_month_hours.csv"

    elif self.state == 4:  # week
      start = start.replace(hour=0, minute=0, second=0, microsecond=0)
      monday = start - timedelta(days=start.weekday())
      satday = monday + timedelta(days=5)

      lc = self.myCalender.findBetween(monday, satday)

      self.LogMessage(f"save week of {monday.strftime('%a %d.%m.%y')}")
      fname = f"{monday.strftime('%y-%m-%d')}_week_hours.csv"

    elif self.state == 3:  #day
      start = start.replace(hour=0, minute=0, second=0, microsecond=0)
      end = start + timedelta(days=1)

      lc = self.myCalender.findBetween(start, end)

      self.LogMessage(f"save day of {start.strftime('%a %d.%m.%y')}")
      fname = f"{start.strftime('%y-%m-%d')}_day_hours.csv"

    else:
      self.LogMessage(f"saving the calender")
      self.myCalender.SaveCal()
      console.hud_alert("calender saved", 'success', 1)
      #   NOTE: console.hide_activity dismisses the hud. return of hud dont resets activity
      # console.hide_activity()
      return

    with open(fname, "w") as f:
      lc.WriteDurationsToCSV(f)

    self.LogMessage(f"File {fname} with hours written")
    console.hud_alert("file saved", 'success', 1)
    #console.hide_activity()

    if self.view['switch_share_hours'].value:
      console.open_in(fname)

    # check if mail hours is set, then generate email with file as attachement

  def seg_view_action(self, sender):
    '''Manage selections in segmented control to chose view of second pane / right tableview
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

  def bt_save_all_action(self, sender):
    """Save all data to the .json and .csv files via memberfunctions of Titra.Calender
        """
    self.myCalender.SaveTasks()
    self.myCalender.SaveProjects()

    #   SaveCalender had problems writing german umlauts "äöüÄÖÜß" !!!

    # - problems when writing german umlauts solved by adding 
    #   encoding='utf8',errors="ignore" to open file in TiTra.py
    #   Why is this only appearing in CSV and not on JSON?

    self.myCalender.SaveCal()

    self.LogMessage("Alles gespeichert: task.json, prj.json, cal.csv")
    # print("Alles gespeichert: task.json, prj.json, cal.csv ",
    #      datetime.datetime.now().strftime("%H:%M:%S"))

  def bt_delete_all_action(self, sender):
    """ DEPrICIATED 
				löschen +/- 70 Tage
		"""
    return
    now = self.view["datepicker"].date

    self.myCalender.removeBetween(
      now - timedelta(days=70), now + timedelta(days=70))
    self.LogMessage(
      f"Alle Actions +/- 70 Tage {self.view['datepicker'].date} gelöscht")

  def bt_backup_action(self, sender):
    """Sollte auch noch vorher alles löschen!
           und die globalen Variablen mit den Listen aller Projekte neu füllen
           
           BRAUCHE ICH die globalen Variablen noch?
           
           BRAUCHE ABER eine Methode Calender.clear()
        """

    now = self.view["datepicker"].date

    self.myCalender.SaveAndRemoveMonth(now, "./")
    self.LogMessage(f"SaveAndRemoveMonth {self.view['datepicker'].date}")

  def bt_read_all_action(self, sender):
    """DEPRECIATED
           Alle Daten aus den Standarddateien lesen
           NICHT vollständig realisiert!
           Sollte auch noch vorher alles löschen!
           und die globalen Variablen mit den Listen aller Projekte neu füllen
        """
    return
    now = datetime.datetime.today()
    now = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    self.myCalender.removeBetween(now, now + timedelta(days=40))

    with open('tasks.json', 'r') as f:
      all_tasks = TiTra.Task.ReadAllTasksFromJSON(f)
    with open('prj.json', 'r') as f:
      all_projects = TiTra.Project.ReadAllProjectsFromJSON(f)

    with open("cal.csv", "r") as f:
      self.myCalender.ReadCalFromCSV(f)

    self.LogMessage(
      "NICHT gelöscht, alles gelesen: task.json, prj.json, cal.csv")

  def bt_add_action(self, sender):
    """Füge eine neue Aktion hinzu und finde aus der aktuellen Selektion 
           den Task, die Task ID heraus. Action erstellen und an g_cal anfügen
        """
    self.LogMessage(f"add sel={self.selected_row} in state {self.state}")

    if self.state == 1 and self.selected_row != -1:
      a = self.selected

      self.LogMessage(f"{a}")

      id = int(a["id"])
      task = TiTra.Task.FindTaskid(id)
      self.myCalender.add(task.NewAction(self.view["datepicker"].date))
      self.CalChanged = True

      #			print("add_action ", datetime.datetime.now().strftime("%H:%M:%S"))
      self.bt_cal2_action(sender)

      now = self.view['datepicker'].date
      self.view["BoxPlotView"].SetActions(
        self.myCalender.UIActionsOfDayList(now))
      self.GetBoxAreaData(None)

  def bt_delete_action(self, sender):
    """DEPRICIATED
		Lösche die selektierte Action aus dem Calender
		"""
    return
    self.LogMessage(f"delete sel={self.selected_row} in state {self.state}")

    if self.state == 2 and self.selected_row != -1:
      a = self.selected

      self.LogMessage(f"{a['date']} {a['time']} {a['title']}")
      #print(a)

      time = datetime.datetime.strptime(f"{a['date']} {a['time']}",
                                        "%Y-%m-%d %H:%M")

      self.LogMessage(time.strftime("%d.%m.%Y %H:%M:%S"))

      self.myCalender.removeBetween(
        time - timedelta(seconds=59), time + timedelta(seconds=59))

      self.bt_cal_action(sender)
      self.bt_cal2_action(sender)

  def bt_now_action(self, sender):
    '''Button now clicked, sets Datepicker to today()
		'''
    d = datetime.datetime.today()
    self.view["datepicker"].date = d

    self.dapi_action(None)
    return

    if self.state == 2:
      self.bt_cal_action(sender)
    elif self.state == 3:
      self.bt_dur_day_action(sender)
    elif self.state == 4:
      self.bt_dur_week_action(sender)
    elif self.state == 5:
      self.bt_dur_month_action(sender)
    self.bt_cal2_action(sender)

  def dapi_action(self, sender):
    '''Some Action in datepicker has happend
           update the content of "tableview1" according to new date
        '''
    # print(f"\n Gewähltes Datum {sender.date}")

    if self.state == 2:
      self.bt_cal_action(sender)
    elif self.state == 3:
      self.bt_dur_day_action(sender)
    elif self.state == 4:
      self.bt_dur_week_action(sender)
    elif self.state == 5:
      self.bt_dur_month_action(sender)
    self.bt_cal2_action(sender)

    now = self.view['datepicker'].date
    self.view["BoxPlotView"].SetActions(
      self.myCalender.UIActionsOfDayList(now))
    self.GetBoxAreaData(None)

  def bt_CopyPy_action(self, sender):
    CopyFileList(("TiTra.py", "TiTraPy.py", "DataSources.py", "TiTraPy.pyui",
                  "TasksProjects.py", "Tasks.pyui", "Projects.pyui"))
    self.LogMessage("Dateien von Entwicklung in Produktion kopiert")

  def GetBoxAreaData(self, sender):
    '''Fetch the data needed to show the BoxAreaPlot
      '''
    start = self.view["datepicker"].date

    start = start.replace(hour=0, minute=0, second=0, microsecond=0)
    start = start - timedelta(days=start.weekday())
    end = start + timedelta(days=7)

    lc = self.myCalender.findBetween(start, end)
    l = lc.UICalcDurations()

    total_area = self.view['BoxAreaPlot'].width * self.view[
      'BoxAreaPlot'].height

    total_h = 0
    for h in l:
      total_h += h["hour"]

    for h in l:
      h['percent'] = h['hour'] / total_h
      h['area'] = round(h['percent'] * total_area)

    l = sorted(l, key=lambda i: (-i['area']))
    self.view["BoxAreaPlot"].SetActions(l)
    self.view["l_BoxArea"].text = "since " + start.strftime("%d.%m.%y") + f" {total_h:5.1f} h" 
  
#    print(f"\nDurations for total {total_h} h\n", l)

  @ui.in_background
  def tv_cal_action(self, sender):
    info = sender.items[sender.selected_row]

    d = self.view["datepicker"].date
    ts = info['time']
    d = d.replace(hour=int(ts[0:2]), minute=int(ts[3:5]))
    self.LogMessage('selected_row {} new date {}'.format(
      sender.selected_row, d.strftime("%a %d.%m %H:%M")))
    self.view["datepicker"].date = d

  @ui.in_background
  def tv_task_action(self, sender):
    info = sender.items[sender.selected_row]
    self.selected = info
    self.selected_row = sender.selected_row

  @ui.in_background
  def tv1_action(self, sender):
    info = sender.items[sender.selected_row]
    console.alert('info',
                  '\n'.join(['{} = {}'.format(i, info[i]) for i in info]))

  def get_available_memory(self):
    """found in github
            what is the original source of this peace of magic?
            https://gist.github.com/lukaskollmer/a09c0278d2d224b9f4839a895ebb9988
            https://forum.omz-software.com/topic/3146/share-code-get-available-memory
		"""

    NSProcessInfo = ObjCClass('NSProcessInfo')
    NSByteCountFormatter = ObjCClass('NSByteCountFormatter')

    class c_vm_statistics(Structure):
      _fields_ = [('free_count', c_uint), ('active_count', c_uint), (
        'inactive_count', c_uint), ('wire_count', c_uint), (
          'zero_fill_count', c_uint), ('reactivations', c_uint), (
            'pageins', c_uint), ('pageouts', c_uint), ('faults', c_uint), (
              'cow_faults', c_uint), ('lookups', c_uint), ('hits', c_uint),
                  ('purgeable_count',
                   c_uint), ('purges', c_uint), ('speculative_count', c_uint)]

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

    HOST_VM_INFO = c_int(2)  # This is a c macro
    KERN_SUCCESS = 0  # Another c macro (No c_int initializer used because we don't pass it to a c function)

    get_host_statistics = host_statistics(host_port, HOST_VM_INFO,
                                          cast(byref(vm_stat), POINTER(c_int)),
                                          byref(host_size))

    if not get_host_statistics == int(KERN_SUCCESS):
      print("Failed to fetch vm statistics")

    mem_used = (vm_stat.active_count + vm_stat.inactive_count +
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
  todir = '../TiTra.prod/'
  fromdir = '../TiTra/'

  if not os.path.exists(fromdir):
    print(f"{fromdir} existiert leider nicht")
  else:

    for fi in filelist:

      print(f"copy {fi}           >> from {fromdir} to {todir}")

      shutil.copy2(fromdir + fi, todir + fi)


global cal

console.clear()

if os.path.exists("prefix.txt"):
  with open("prefix.txt", "r") as f:
    prefix = f.readline()[0:-1]
#    print (f"\n** prefix.txt gefunden prefix='{prefix}'\n") 
  cal = TiTra.Calender(prefix)
else:
  cal = TiTra.Calender("test")

# here can result a problem, if done in other sequence
cal.LoadTasks()
cal.LoadProjects()
cal.LoadCal()

s = ShowTableView(cal)

