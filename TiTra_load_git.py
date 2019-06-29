# TiTra_load.py
#


import requests as r
import os
import shutil

if not os.path.exists('TiTra'):
    os.makedirs('TiTra')

filelist=( "TiTraPy.py", "TiTraPy.pyui"
         , "DataSources.py"
         , "TiTra.py"
         , "README.md"
         )
todir='./'
fromurl='https://raw.githubusercontent.com/ArduFox/TiTraPy/master/'

# first backup
for fi in filelist :
    if os.path.exists(todir+fi):
        print(f"backup {fi}           >> in {todir}")
        shutil.copy2(todir+fi,todir+fi+".bak")

for fi in filelist :
    
    print(f"loading {fi}      \t\t>> from {fromurl} to {todir}")
    o=open(todir+fi,'wb'); 
    b=o.write(r.get(fromurl+fi).content); 
    print(f"                       \t\t\t{b} bytes loaded")
    o.close()
    
