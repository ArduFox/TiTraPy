# TasksProjects.py
#
# part of TiTraPy = TimeTracker for pythonistas
#
# Stubble to edit Tasks and Projects and save the .json files when done
#
# new in V 00.20
# - jump to the project selected in tasks or to the new created project
# - new task & new project do work
# - detect if changes in mask / fields are made  by comparing values and copy textfields to object instances
# - save all tasks and projects to files
# - if Project of Task changes: find instance of new project, call Task.SetProject(instance)
#
# TODO
# - Propagate name changes in project into all tasks of that project -> should be done in TiTra.py
# - Delete task / project. Project only deletable when without tasks? Tasks only deletable when unused in actions?
#
#
# TODO in TiTra.py
# - Implement RemoveTask
# - Implement RemoveProject
# - Implement Rename Project


import ui, dialogs
import os, sys
import TiTra


version = '00.20'

# https://gist.github.com/danrcook/5b35e47628d28daec1d5ec7e909b4f95

# https://forum.omz-software.com/topic/3353/share-code-sliderwithlabel-class-for-ui-slider-featuring-editable-label

'''
SliderWithLabel is a wrapper for ui.Slider() for use in Pythonista on iOS. Provides an editable label for the display and setting of the slider value.

See SliderWithLabel class for detailed usage.
'''

__author__ = '@cook'

import ui

class SliderWithLabel(ui.View):
	'''wrapper for ui.Slider to also show a label. You can edit the value of the slider directly in the label since it is a textfield. Can take the following keyword arguments:
	- for the slider:
	>> value: default value when presented (should be a number that is less than max_val and greater than 0). The default is 50
	>> max_val: the default for a usual slider is 1.0. SliderWithLabel will conventiently multiply the max_val for the label display and for returning it's value attribute. The default is 100
	>> tint_color for the color of the slider bar (up to current point). Default is 0.7 (gray)
	- values are rounded in the label and for SliderWithLabel.value
	- SliderWithLabel needs some vertical space: has a height of 60
	- use SliderWithLabel.value for return a value between 0 and SliderWithLabel.max_val
	
	Delegate: use an object with a method of value_did_change and set SliderWithLabel.delegate'''
	
	def __init__(self, **kwargs):
		self.frame = kwargs['frame'] if 'frame' in kwargs else (0,0,100,60)
		self.slider = ui.Slider()
		self.max_val = kwargs['max_val'] if 'max_val' in kwargs else 100
		self.slider.value = kwargs['value']/self.max_val if 'value' in kwargs else 0.5
		self.value = round(self.slider.value*self.max_val) #for convenience in getting the value attribute
		self.slider.action = self.update_label_and_value
		self.slider.tint_color = kwargs['tint_color'] if 'tint_color' in kwargs else 0.7
		self.label = ui.TextField()
		self.label.action = self.update_value
		self.label.bordered = True
		self.label.alignment = ui.ALIGN_CENTER
		self.label.font = ('<system>',11)
		self.label.text_color = kwargs['text_color'] if 'text_color' in kwargs else 0.7
		self.label.text = str(self.value+1)
		self.add_subview(self.slider)
		self.add_subview(self.label)
		
	def update_value(self, sender):
		try:                    #try/except in case wrong text is entered...
			self.slider.value = int(self.label.text)/self.max_val
			self.update_label_and_value(self)
		except:
			pass
			
	def set_max(self, m:int):
		self.max_val=m
		self.label.text = str(self.value+1)
		self.slider.value=self.value/self.max_val
		self.update_label_and_value(self)
								
	def set_value(self, v: int):
		self.value = v
		self.label.text = str(self.value+1)
		self.slider.value=self.value/self.max_val
		self.label.x = (self.slider.width - 34) * self.slider.value - (self.label.width/2) + 17		
		if self.label.x + self.label.width > self.width:
			self.label.x = self.width - self.label.width
		if self.label.x < 0:
			self.label.x = 0			

	def update_label_and_value(self, sender):
		self.label.x = (self.slider.width - 34) * self.slider.value - (self.label.width/2) + 17
		self.value = round(self.slider.value*self.max_val)
		self.label.text = str(self.value+1)
		if self.label.x + self.label.width > self.width:
			self.label.x = self.width - self.label.width
		if self.label.x < 0:
			self.label.x = 0
		#for delegate
		if self.delegate and hasattr(self.delegate, 'slider_value_did_change'):
			if callable(self.delegate.slider_value_did_change):
				self.delegate.slider_value_did_change(self.value)
				
	def draw(self):
		self.height = 60
		self.slider.frame = (0,self.height/2-7,self.width, 34)
		self.label.width, self.label.height = 46, 20
		self.label.y = self.slider.y - (self.label.height + 2)
		self.label.x = (self.slider.width - 34) * self.slider.value - (self.label.width/2) + 17
		


class SliderValueChangeDelegate():
  def __init__(self, TPEdit ):
    self.tpe=TPEdit
    
  def slider_value_did_change(self, value):
    self.tpe.slider_moved(value)

def slider_expample():
	#simple example with three sliders and a delegate to update the view name with the slider value.
	
	view = ui.View()
	
			
	value_change = SliderValueChangeDelegate()
	
	w = ui.get_screen_size()[0]
	a = SliderWithLabel(frame=(10,30,w-20,60), value=30, max_val=300)
	a.delegate = value_change
	b = SliderWithLabel(frame=(10,90,w-20,60), value=75, max_val=100)
	b.delegate = value_change
	c = SliderWithLabel(frame=(10,150,w-20,60), max_val=1000)
	c.delegate = value_change
	view.add_subview(a)
	view.add_subview(b)
	view.add_subview(c)
	view.background_color = 1
	view.present()


#. ----- END Slider ----------

class TPEditor(object):
  
  def __init__(self, cal: TiTra.Calender):
    self.view = ui.load_view('Tasks.pyui')
    self.view.name="Tasks"
    self.__cal=cal
    self._allTasks=TiTra.Task.GetAllTasksList()
    self._allProjects=TiTra.Project.GetAllProjectsList()
    self._index=0
    self.nav_view=ui.NavigationView(self.view)
    self.nav_view.navigation_bar_hidden=True
    self.__len=len(self._allTasks)
    
    root, ext = os.path.splitext(sys.argv[0])  # script path without .py
#    script_name = os.path.basename(root)  # script name without the path
    listOfDirs = root.split('/')
    l = len(listOfDirs) - 1
    version_button = ui.ButtonItem()
    version_button.title = f"{listOfDirs[l-1]}/{listOfDirs[l]} V {version}"
    version_button.tint_color = 'red'
    self.view.right_button_items = [version_button]
            
#    self.nav_view.present('sheet')
    self.nav_view.present()
    self.slider = SliderWithLabel(frame=(61,18,337,60), value=0, max_val= len(self._allTasks)-1)
    value_change = SliderValueChangeDelegate(self)
    self.slider.delegate = value_change
    self.view.add_subview(self.slider)
    self.populate()
        
  def populate(self):  
    if self.view.name=="Projects":
          
      self.view['tf_name'].text=self._allProjects[self._index]._name
      self.view['tf_symbol'].text=self._allProjects[self._index]._emoij
      self.view['tf_color'].text=self._allProjects[self._index]._farbe    
      
      self.view['l_id'].text="-"      # str(self._allProjects[self._index]._id)
      self.view['l_count'].text=f"{self._index+1} of {self.__len}"
      self.view['l_colorbox'].bg_color=self._allProjects[self._index]._farbe
    else:
      #print (f"i={self._index} of {len(self._allTasks)} = self.__len")
      self.view['tf_name'].text=self._allTasks[self._index]._name
      self.view['tf_symbol'].text=self._allTasks[self._index]._emoij
      self.view['tf_project'].text=self._allTasks[self._index]._projectName    
      self.view['tf_color'].text=self._allTasks[self._index]._farbe    
      
      self.view['l_id'].text=str(self._allTasks[self._index]._id)
      self.view['l_count'].text=f"{self._index+1} of {self.__len}"
      self.view['l_colorbox'].bg_color=self._allTasks[self._index]._farbe
      #print(f"index={(self._index+1)} slider={round((self._index+1)/len(self._allTasks)*1000)/1000} len={len(self._allTasks)}")
    
  def check_and_copy(self):
    if self.view.name=="Projects":
      if (self.view['tf_name'].text   != self._allProjects[self._index]._name or
         self.view['tf_symbol'].text != self._allProjects[self._index]._emoij or
         self.view['tf_color'].text  != self._allProjects[self._index]._farbe)    :
          
        self._dirty=True
        self.bt_save(None)
    else :
      if (self.view['tf_name'].text    != self._allTasks[self._index]._name or
         self.view['tf_symbol'].text  != self._allTasks[self._index]._emoij or
         self.view['tf_project'].text != self._allTasks[self._index]._projectName or
         self.view['tf_color'].text   != self._allTasks[self._index]._farbe)    :
          
        self._dirty=True
        self.bt_save(None)                    
    
  def bt_right(self,sender):
    if self._index < self.__len -1  :
      self.check_and_copy()
      self._index += 1
      self.populate()
      self.slider.set_value(self._index)
      
  def bt_left(self,sender):
    if self._index > 0 :
      self.check_and_copy()
      self._index -= 1
      self.populate()
      self.slider.set_value(self._index)
            
  def bt_new_task(self,sender):
    if self.view.name=="Projects":
      p=TiTra.Project("?")
      self._allProjects=TiTra.Project.GetAllProjectsList()
      self.__len=len(self._allProjects)
      i=0
      for p in self._allProjects:
        if p._name=="?" :
          self._index=i
          break
        else :
          i+=1
      # self.__index=?      find Project("?") in newly sorted list
    else:
      t=TiTra.Task("?")
      self._allTasks=TiTra.Task.GetAllTasksList()
      self.__len=len(self._allTasks)
      self._index=self.__len-1
      
    # _index 0 to (len -1)
    # labels and label over slider always shows (_index = value) +1   -->. 1 to len 
    
    print(f"new {self.view.name}: len={self.__len} i={self._index}")    
    self.slider.set_value(self._index)
    self.slider.set_max(self.__len-1)
    self.populate()
    
  def bt_new_project(self,sender):
    pass
      
  def bt_save(self,sender):
    '''save changes in the textfield to tasks or project object / instance
    '''
    if self.view.name=="Projects":
      if self._allProjects[self._index]._name != self.view['tf_name'].text :
        self._allProjects[self._index]._name = self.view['tf_name'].text
        # TODO Update all tasks of this project -> in TiTra.py?
        
      self._allProjects[self._index]._emoij=self.view['tf_symbol'].text
      self._allProjects[self._index]._farbe=self.view['tf_color'].text
      self.view['l_colorbox'].bg_color=self._allProjects[self._index]._farbe
      print(f"")
    else:
      self._allTasks[self._index]._name=self.view['tf_name'].text
      self._allTasks[self._index]._emoij=self.view['tf_symbol'].text
      self._allTasks[self._index]._projectName=self.view['tf_project'].text
      # find instance of project in self._allProjects
      prj=None
      for p in self._allProjects:
        if p._name==self.view['tf_project'].text :
          prj=p
          break

      if prj != None :
        self._allTasks[self._index].SetProject(prj)      
                      
      self._allTasks[self._index]._farbe=self.view['tf_color'].text
      self.view['l_colorbox'].bg_color=self._allTasks[self._index]._farbe
    print(f"save {self.view.name}: {self.view['tf_name'].text} len={self.__len} i={self._index}")    
              
  def bt_delete(self,sender):
    if self.view.name=="Projects":
      self.__len=len(self._allProjects)
      # find project instance
      prj=None
      for p in self._allProjects:
        if p._name==self.view['tf_project'].text :
          prj=p
          break

      if prj != None :
        prj.RemoveProject()                          
        
    else:    
      self.__len=len(self._allTasks)    
      # TODO be very carefully what to do, when deleting tasks
      # Deleting tasks can lead to inconsistent actions in calender
      # therefore ask for permission before actually deleting
    
  def bt_save_all(self,sender):
    '''save tasks and projects
    '''
    self.__cal.SaveTasks()
    self.__cal.SaveProjects()
    
    
    print(f"Files saved {self.__cal.GetPrefix()}: Tasks ({len(self._allTasks)}) & Projects ({len(self._allProjects)})")
    
  def bt_select_project(self,sender):
    # no function in TiTra to list all projects !! 
    
    # Present a list of items and return the one(s) that were selected. When the dialog is cancelled, None is returned. 
    # The items list can contain any kind of object that can be converted to a string. 
    # To get more control over how each item is displayed in the list, you can also use 
    # a list of dictionaries (see ui.ListDataSource.items for details).
    
    erg=dialogs.list_dialog(title='select project', items=TiTra.Project.UIProjectList(), multiple=False)
    
    if None != erg:
      self.view['tf_project'].text=erg

  def bt_edit_tasks(self,sender):
    '''Return to editing tasks
    '''
    self.view=self.t_view
    self.slider=self.t_slider
    self._index=0
    self.__len=len(self._allTasks)        
    self.populate()
    self.slider.set_value(self._index)
    self.nav_view.pop_view()

  def bt_edit_proj(self,sender):
    '''Change to editing projects
    '''
    v = ui.load_view('Projects.pyui')
    
    v.background_color = 'lightcyan'
    v.name = 'Projects'
    self.t_slider=self.slider
    self.slider = SliderWithLabel(frame=(61,18,337,60), value=0, max_val= len(self._allProjects)-1)
    value_change = SliderValueChangeDelegate(self)
    self.slider.delegate = value_change
    v.add_subview(self.slider)
    
    i=0
    self._index=i
    for p in self._allProjects:
      if p._name==self.view['tf_project'].text :
        self._index=i
        break
      else :
        i+=1
            
    self.t_view=self.view
    self.view=v
    self.slider.set_value(self._index)
    self.__len=len(self._allProjects)        
    self.populate()
    
    # puts the actual visible view on "stack"
    # and shows this newly created view
    # and - hopefully - shows a back button
    self.nav_view.push_view(v)    
    

  def slider_moved(self, value:int):
#    print (f"moved {value} {self._index}")
    if self._index != value :
      self.check_and_copy()
      self._index=value
      self.populate()                                    
         
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
# cal.LoadCal()

TPEditor(cal)

# v = ui.load_view('TasksProjects.pyui')
# v.present('sheet')
