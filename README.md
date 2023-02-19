# Haushaltsbot
 Discord Bot um den Haushalt zu regeln.

## Allgemeine Informationen
Der Haushaltsbot nutzt eine SQLite um den Kalender zu verwalten.
Die Haushaltsaufgaben werden in einem Array gespeichert und bei der Zuteilung zufällig auf die Mitglieder zugeteilt.
(Fast) jede Outputmessage des Bots beginnt mit einem Emoji.
Die Befehle sind mit den neuen /-Befehlen umgesetzt.

## Organisation auf Discord
Es werden folgende Rollen benötigt:
- Haushaltsmitglied
- Abwesend
- Mülldienst

Wenn der Bot nur einen Channel für alles verwenden soll, gib für die Channel_IDs immer den gleichen Channel an. Ich empfehle mehrere Channels um den Überblick zu wahren.

## Daily-Nachricht
Jeden Tag zu einer festgegeben Uhrzeit gibt der Bot eine tägliche Nachricht aus. Dabei prüft er folgendes ab:
- Am Anfang des Monats gibt er alle Termine in diesem Monat an. Sowie den Erst- und Ausweichtermin für den Großputztag
    - Alternativ 1: Anfang der Woche gibt er nur die Termine der Woche an. Handelt es sich um eine geraden Kalenderwoche so erstellt der Bot eine neue Haushaltszuteilung aus.
    - Aternativ 2: Bei jedem anderen normalen Wochentag gibt der Bot die Termine am jeweiligen Tag aus.
- Ob am nächste Tag oder in einer Woche das Altpapier eingesammelt wird, um daran zu erinnern.
- Ob jemand geburtstag hat und gratuliert in diesem Fall.
- Handelt es sich um ein Freitag wird daran erinnert die Pflanzen zu gießen.
---
## Befehle
### Zuteilung
*Funktion:* 
>Erstellt eine neue Haushaltszuteilung unter den Haushaltsmitgliedern.

*Return:* 
>Die neue Zuteilung als Nachricht.

### Single_Event
*Parameter:*
>``datum`` -> Datum für das Event\
``eventname`` -> Name für das Event\
``eventinfo`` -> Informationen zum Event

*Funktion:* 
>Erstellt einen einzelnen Termin und trägt diesen in den Kalender (die Datenbank) ein.

*Return:*
>Erfolgsmeldung beim erfolgreichen Schreiben in die Datenbank. Andernfalls eine Fehlermeldung.\
Fehlermeldung auch bei falschen Eingaben.

### Multiple_Events
*Parameter:*
>``datum`` -> Datum für die Events\
``eventname`` -> Name der Events durch ``;`` separiert\
``eventinfo`` -> Informationen zum den jeweiligen Events ebenfalls durch ``;`` separiert

*Funktion:* 
>Erstellt mehrere Termine für einen Tag und trägt dies in den Kalender ein.

*Return:*
>Erfolgsmeldung beim erfolgreichen Schreiben in die Datenbank. Andernfalls eine Fehlermeldung.\
Fehlermeldung auch bei falschen Eingaben. 

### Repeated_Events
*Parameter:*
>``eventname`` -> Name für das Event\
``eventinfo`` -> Informationen zum Event\
``dates`` -> Alle Daten wo das Event stattfindet mit einen Leerzeichen separiert.

*Funktion:* 
>Erstellt einen Termin für die jeweiligen angegebenen Daten und trägt diese in den Kalender ein.

*Return:*
>Erfolgsmeldung beim erfolgreichen Schreiben in die Datenbank. Andernfalls eine Fehlermeldung.\
Fehlermeldung auch bei falschen Eingaben.

### Eventserie
*Parameter:*
>``datum`` -> Startdatum für die Events\
``eventname`` -> Name der Events \
``eventinfo`` -> Informationen des Events\
``abstand`` -> Abstand den die Events zueiander haben, angegeben durch eine Zahl direkt gefolgt von ``d`` oder ``w`` oder ``m`` oder ``y``\
``anz_wdh`` -> Anzahl wie oft das Event sich wiederholen soll

*Funktion:* 
>Erstellt mehrere Termine beginnend ab ``datum`` in dem angegeben Abstand.

*Return:*
>Erfolgsmeldung beim erfolgreichen Schreiben in die Datenbank. Andernfalls eine Fehlermeldung.\
Fehlermeldung auch bei falschen Eingaben.

### Delete_Events
*Parameter:*
>``ids`` -> die IDs der zu löschenden Events.

*Funktion:*
>Löscht die Einträge mit den angebenen IDs in der Datenbank-

*Return:*
>Erfolgsmeldung beim erfolgreichen Schreiben in die Datenbank. Andernfalls eine Fehlermeldung.\
Fehlermeldung auch bei falschen Eingaben.

### Add_Bday
*Parameter:*
>``datum`` -> Datum des Geburtstages\
``name`` -> Name der Person 

*Funktion:*
>Erstellt einen Eintrag zum angegeben ``datum`` mit dem Eventname "Geburtstag" und ``name`` als Eventinformation in der Datenbank.

*Return:*
>Erfolgsmeldung beim erfolgreichen Schreiben in die Datenbank. Andernfalls eine Fehlermeldung.\
Fehlermeldung auch bei falschen Eingaben.

### Abwesenheit
*Parameter:*
>``von_datum`` -> Startdatum der Abwesenheit\
``bis_datum`` -> Enddatum der Abwesenheit 

*Funktion:*
>Erstellt einen Eintrag zum angegeben ``von_datum`` mit dem Eventname "Abwesenheits_start" und die UserID der Person als Eventinformation in der Datenbank. Sowie ein Eintrag zum ``bis_datum`` mit dem Eventname "Abwesenheits_ende".\
Dies Nutzt der Bot um an dem Startdatum der Person die Abwesenheitsrolle zu geben und am Enddatum diese Rolle wieder zu entfernen.

*Return:*
>Erfolgsmeldung beim erfolgreichen Schreiben in die Datenbank. Andernfalls eine Fehlermeldung.\
Fehlermeldung auch bei falschen Eingaben.

### Monats_Übersicht
*Parameter:*
>``monat`` -> Zahl des Monats dessen Übersicht man sehen möchte

*Funktion:*
>Erstellt eine Monatsübersicht mit allen Terminen im angegebenen ``monat``.

*Return:*
>Die Monatsübersicht als Nachricht.

### Wochen_Übersicht
*Parameter:*
>``kalenderwoche`` -> Kalenderwoche dessen Übersicht man sehen möchte

*Funktion:*
>Erstellt eine Wochenübersicht mit allen Terminen in angegebenen ``kalenderwoche``.

*Return:*
>Die Wochenübersicht als Nachricht.



### Pet
>Hiermit kannst du dem Bot etwas zuneigung zeigen.

### Help
*Return:* 
>Gibt eine Hilfestellung zum Umgang mit den Befehlen zurück.

### Help_Taks
*Parameter:*
>``task`` -> Den Task zu dem man Erklärung benötigt.

*Return:* 
>Gibt die Erklärung zu dem angegeben Task an.

### Jasdebug
*Parameter:*\
>``todo`` -> Auszufürhrenden Debug-Befehl\
``debugdate`` -> Datum zum Debuggen\

*Funktion:* 
>Je nach dem angegeben ``todo``:
>- clear -> löscht den gesamten Kalender
>- Show all -> zeigt den gesamten Kalender Inhalt an, so wie der aus der Datenbank genommen wird
>- time -> gibt die aktuelle Zeit, sowie die Uhrzeit für den Daily-check aus
>- daily -> führt die Daily Routine für den angegeben Debugdate aus
>- altpapier -> Macht einen Altpapiercheck

*Return:* 
>Entsprechend der Funktion