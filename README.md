# TiTraPy
TimeTracker in python for pythonista on IOS

# State

Testing new repository to publish my ongoing work in progress

Code and Documentation are mixed in German and English, but mostly German!

# ToDo

# Aktueller Stand

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
