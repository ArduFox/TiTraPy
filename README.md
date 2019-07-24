# TiTraPy
**Ti**me **Tra**cker in python for pythonista on IOS

Main file is TiTraPy.py, which uses pythonista environment and libs in IOS

TiTra.py contains classes for the "business logic" and can be tested and used in standard python emvironments

# State

Code and Documentation are mixed in German and English, but mostly German!
Started the first [stubble](doc.md) of user manual and code documenation in doc.md

# urls to raw files

Do they ever change? Don't think so

* [https://raw.githubusercontent.com/ArduFox/TiTraPy/master/TiTra.py](https://raw.githubusercontent.com/ArduFox/TiTraPy/master/TiTra.py)
* [https://raw.githubusercontent.com/ArduFox/TiTraPy/master/TiTraPy.py](https://raw.githubusercontent.com/ArduFox/TiTraPy/master/TiTraPy.py)
* [https://raw.githubusercontent.com/ArduFox/TiTraPy/master/TiTraPy.pyui](https://raw.githubusercontent.com/ArduFox/TiTraPy/master/TiTraPy.pyui)

# ToDo

* Publish to 
* :ok: Stubble of a tool to edit tasks and projects -> TasksProjects.py
* :ok: Make class Calender containing all Tasks, Projects and Actions
* New Name for class ShowTView >> TiTraPyGUI & :ok: rename pyui file
* rework test.py - test everything and translate / give useful feedback about tests
* :ok: Add Tool to download the 3 main files (Titra.py, TiTraPy.py, TiTraPy.pui, DataSources.py, TiTra.py,README.md) from this git 
* :ok: DataSources dont have access to global var g_cal for delete entries! New class variable in ShowTView!
* :ok: Transport File [VersionInStatusBar](https://github.com/cvpe/Pythonista-scripts/blob/dfbf9c4ee8172138b4b64c760f89cea1ed5562df/VersionInStatusBar.py) to this git or integrate in own code
* :ok: remove ShowTView Files
* :ok: collect and publish code for testing classes in TiTra.py
* :ok: write a short but instructive user manual - even if it will bei soon outdated

# Status

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


## 21.06.2019

* TiTraPy.py enthält jetzt den aktuellen Code für die UI und die Anwendung und die DOCStrings darin sind verbessert and mostly in english
* DataSources.py enthält meine drei DataSources
* BEIDES GETESTET :ok: 

## 18.06.2019 Nutzung im realen Leben

Ich nutze das Tool bereits im realen Leben und notiere, was mir auffällt

* Save nach schließen über X funktioniert nicht zuverlässig. In der Console sehe ich den print aus der Routine aber nach wieder öffnen sind neue Einträge nicht mehr da. Wenn ich aktiv den save button nutze, dann klappt es
* Blöd ist auch, dass ich nach X auf die Console zurückfalle und zwei aktive Anwendungen sehe.
* Bei mehrfachem Aufruf des Shortcuts kann ich auch mehrere TiTras hintereinander sehen / schließen
* In der Section / Titel sollte auch das Datum angezeigt werden. Dafür ggf. über parent nach oben bis Datepicker hangeln
* save work funktioniert mit den beiden Tabellen auch nicht mehr sinnvoll
* Die beiden Tabellen stilistisch etwas unterschiedlich gestalten
* für iPhone ein alternatives Layout erstellen mit beiden Tabellen untereinander
* Anleitung.md als Minibedienungsanleitung erstellen
* Ansonsten ist die Anwendung stabil
* Pflege und Änderung von Tasks und Projekten zunächst als eigene Anwendung? Das würde es erstmal einfacher machen
    * Darin sollte das Nullprojekt obligatorisch sein und nur anders gestaltet werden können.


## 15 & 16.06.2019 ShowTView

* in `Action._init_` die Zeit auf Sekunden=0 und Mikrosekunden=0 geglättet
* Action neue Vergleichsfunktionen __eq__ __ne__ die vorher auf None testen 
* Views sehen jetzt richtig hübsch aus inkl **swipe delete** für Calender
* Neue Funktionen removeIDAtTime und UICalcDuration  -  läuft :+1:
* Speicherfunktionen [`get_available_memory(self):`](https://gist.github.com/lukaskollmer/a09c0278d2d224b9f4839a895ebb9988) von Lukas Kollmer in den Code integriert, sie schreiben sauber ins visuelle Log - es wird immer wieder Speicher freigegeben!
* Weniger Glück hatte ich mit `VersionInStatusBar` das ich "nur" importiere. Die prints zeigen mir, dass der Code ausgeführt wird aber aus irgendeinem Grund taucht das zusätzliche Label nicht auf
* Drei eigene Klassen abgeleitet aus `ui.ListDataSource` entwickelt. Diese setzen in der Cell eiegen zusätzliche Labels ein, um ein mehrspaltiges Layout hinzubekommen. Außerdem wird in jeder zweiten Zeile der Hintergrund eingefärbt - schön - und Stunden > 15 % rot eingefärbt und ein Section Titel mit Inhalt inkl. Summe der Stunden angezeigt
    * MyTaskDataSource für die Tasks - hat noch keinen geeigneten Input aus
    * MyCalDataSource für den Calender bzw. die Actions
    * MyDurDataSource für die errechneten Dauern



## 14.06.2019 ShowTView

* Experimentiere in pythonista mit der UI und lerne dazu
    * Für TableView die eine eigene Subklasse der Datenklasse "ListDataSource" erstellt, die dann auch eine Subview mit zusätzlichem Label für die Dauer anlegt. Damit ist beispielweise auch eine abwechselnde Unterlegung der Zeilen mit Hintergrundfarben möglich.
    * Weiß auch wie ich Farben und Fonts von Zellen der Tableview ändere
* Ein schwach [strukturtiertes Git](https://github.com/tdamdouni/Pythonista) mit sehr viel Pythonista Code gefunden - einiges auch schon bekannt inkl. der Beispielprogramme aus Pythonista bzw. aus der Doku
* Memory Funktionen [aus dem git](https://github.com/tdamdouni/Pythonista/tree/master/memory) integrieren - frisst meine App den Speicher?

### Weitere Erkenntnisse und todos

* Der Calender enthält nicht auch die Tasks und Projekte. Es könnte nützlich sein dort alles enthalten zu haben und ggf. mindestens die classmethoden auch via Calender Instanzmethoden aufrufen zu können. Dann könnte mit einer Referenz auf einen Calender (der braucht dann ggf. auch einen Namen eines Unterverzeichnisses!) alles in einer „Schachtel“ komplett übergeben werden
* MyListDataSource braucht eine Referenz auf die Instanz von ShowTView, um z.B. auch das Logging nutzen zu können.
* MyListDataSource sollte ggf. besser auf das ursprüngliche Dict von Calender / Report zugreifen als auf das verstümmelte der ListView dings. Andererseits werde ich in meiner MyListDataSource sowieso mich teilweise oder stark von der Listview lösen
* MyListDataSource muss auch auf den Calender / die Tasks zugreifen können
* Für Löschen von Actions ist es nötig neben Zeiten auch IDs zu kennen und zu beachten
* Eingabe von Action geht besser, wenn man Calender & Tasks gleichzeitig sieht: Andere Ansicht oder zusätzliche TableView?
* Button jetzt, der Datum und Uhrzeit auf jetzt setzt ODER addActionNow als Button

#### Sinnvolle Ansichten:
1. Editieren Kalender inkl. Taskliste und Calenderansicht + Termine im Apple Kalender? Da würde ggf. ein Textfeld für Datum und ein TimePicker ausreichen. Zugriff auf den Apple Calender gibt es nicht als Modul in pythonista aber [hier](https://github.com/tdamdouni/Pythonista/blob/master/_2016/pythonista-scripts-lukaskollmer/ical/ical.py) gibt es ein Skript, das das leisten soll
2. Anschauen Berichte zu Zeiten + speichern der Ergebnisse + ggf. email (csv und Text)
4. Editieren von Tasks und Projects und sonstige Wartungsfunktionen


## 10.06.2019 pythonista und TiTra

* ShowTView.py und .pyui angelegt und läuft auch schon
* Transferiere die Dateien per Mail / Webserver hierer
* Eine Produktionsvariante angelegt und die Dateien haben Gamma-Stand erreicht, d.h kurz for Beta Version. Will ich schon produktiv in der LBS nutzen

todo

* Kopiertool verfeinern und Test auf vorhanden und jünger im Zielverzeichnis einbauen! Wo hatte ich das hier am PC?
* README.md auch auf den PI und das iPad transportieren


## 09.06.2019 pythonista und TiTra

* pythonista läuft mit einer ersten einfachen UI - noch zu wenig dokumentiert
* Habe zusätzlich Funktionen in TiTra eingefügt und getestet, die Listen aus Dicts ausgeben als Basis für die Listviews
    * :white_check_mark: ✔️ classmethod Task.UITasksList()
    * :white_check_mark: ✔️ method Projet.UITasksList
    * :white_check_mark: ✔️ method Calender.UIActionsOfDayList(self, day:datetime)    
* Daher gibt es auch eine neue Datei TiTra_UITests.py

:recycle: BackupTool in pythonista ändern, so dass ein zip von TiTra gemacht und vom Server angeboten wird!

:recycle: Ich sollte mal überlegen und programmieren, wie ich die Dateien auf github öffentlich bereitstelle und von dort auf iPad lade. Denn dort sind sie sowieso gespeichert!


## 08.06.2019 TiTra.py und Freunde

* SaveAndRemoveMonth realisiert und getestet
* prints und Docstrings verbessert

## 02.06.2019 TiTra.py und Freunde davon

* TiTra Klassen und Tools in eigener Datei gekapselt
* Juypter Notebook (TiTra Games) angelegt und darin interaktiv die Klassen getestet
    * Erste Erfahrungen mit assert
    * Gezielte Test gebaut
    * Gelernt, wie man Module neu lädt und Dateien kopiert
    * Erste Grafik aufgebaut, die einen Tag in Boxen zeichnet und darstellt als SVG
    * 
* Auf den privaten *iPad* geladen und dort läuft `TiTra_test.py` auch wunderbar in Phytonista!



## Anforderungen an die Anwendung

* Start Stop Aktivität
* Aktivitäten in zwei Levels: 
    * Projekt
    * Tätigkeit
* Editieren von Tätigkeiten:
    * Ändern der zuegeordneten Aktivität
    * Ändern Start oder Endezeitpunkt
    * Wahl des bearbeiteten Tages
    * Ändern auch in vergangenen Tagen
* Ändern von Projekten und Tätigkeiten. Namensänderung wirkt sich auf alle erstellen Zeiteinträge aus
* Start z.B. um 9:00 der Standardaktivität
* Ende aller Aktivität z.B. um 23:00 ?? Will ich das wirklich? Als stets aktiver "Stopper" oder einmal am Tag beim Wechsel auf den nächsten?
* Liste der heute bebuchten Aktivitäten mit Summe der Zeiten
* Export in z.B. CSV der Zeiten für definierten Zeitraum. Standard sind Woche und Monat

## Lösungen

* JSON Datenbanken mit zwei Tabellen
    * Projekte und Tätigkeit
        * Mit den Eigenschaften: Projektname, Farbe, Emoji, Name, ID?
    * Aktivitäten mit
        * Starttermin (Tag und Stunde Minute), ID oder Name

* Anzeige der Listen der bisherigen Tageseinträge, anklickbar, änderbar
* Anzeigen der Liste der Tätigkeiten, anklickbar, änderbar

## Speicherung

* JSON oder csv als Format
    * Mir scheint JSON robuster und ggf. einfacher erweiterbar / aufwärtskompatibel, falls ich die Klassen erweitere
    * Ich verstehe aber noch zu wenig, wie JSON jenseits von einfachen Strukturen funktioniert
    
* Grundprinzipien wären dann
    * Es können keine Referenzen gespeichert werden, sondern nur IDs. D.h. diese IDs müsste ich generieren, aus den Referenzen auslesen (da werden meist Adressen angezeigt?).
    * Beim Einlesen sollte ich die IDs wieder durch Referenzen ersetzen, d.h. ich brauche dict die das leisten für alle Objekte einer Klasse
    * Beim Schreiben wird eine für JSON verwendbare Struktur, nach ähnlicher Systematik wie `__str__` geschaffen, d.h. eine Liste oder ein Dict ohne Referenzen geliefert.
    * Beim Lesen müssten diese Strukturen dann per Iterator wieder die Objektstruktur aufbauen
        * Dabei ist die Reihenfolge wichtig
        * Objekte auf die referenziert werden zuerst:
            1. Task
            2. Project
        * Objekte, die selbst referenzieren später 
            1. Action
