###_IMPORTS --------------------------------------------------------
import os
import re
import random
import discord
import asyncio
import sqlite3
from dotenv import load_dotenv
from discord import app_commands, Intents, Client, Interaction
from datetime import date, time, datetime, timedelta

load_dotenv()

class UtilBot(Client):
    def __init__(self, *, intents: Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self) -> None:
        await self.tree.sync()
client = client = UtilBot(intents = discord.Intents.all())


###_VARIABLES ------------------------------------------------------
guild_id = int(os.getenv("GUILD")) #ChaotenWG                                          1001945324258066462 #mein Server

member_role_id = int(os.getenv("BIGBRAINTME")) #ChaotenWG                                       1033151070333063269 #auf meinen Server
abwesend_role_id = int(os.getenv("ABWESENDROLLE")) #ChaotenWG                                 1070791409990369351 #auf meinem Server
trashtracker_role_id = int(os.getenv("TRASHTRACKER"))  #CWG

haushalt_channel_id = int(os.getenv("HAUSHALT")) #CWG
input_channel_id = int(os.getenv("INPUT")) # 1033144495065284678 #zu "kalender_eintrag"-channel ID umändern
output_channel_id = int(os.getenv("OUTPUT")) # 1033144495065284678 #zu "kalender_ausgang"-channel ID umändern

kalender_name = os.getenv("DBNAME")

data = []
WHEN = time(9, 0, 0)
line = "----------\n"
date_regex = r"^((?:(?:0[1-9]|[12][0-9]|3[01]|[1-9])\.(?:0[1-9]|1[012]|[1-9])\.(?:20)?\d\d)|heute|morgen)$"
datum_liegt_in_der_vergangenheit = ":question: Dein Datum liegt in der Vergangenheit. Leider kann ich nicht zeireisen :pleading_face:"

home_members = []
zuteilung = ""
tasks = ["Küche", "Bad", "WCs", "Boden"]

###_DEBUGGING ------------------------------------------------------
#create new database
# con = sqlite3.connect(kalender_name)
# cursor = con.cursor()
# cursor.execute("CREATE TABLE event(date, year, month, week, name, info, author, entrydate)")
# con.close()
@client.tree.command(name = "jasdebug", description="Debug Command for Jas")
async def jasdebug(interact: Interaction, todo: str, debugdate: str):
    if(interact.user.id == int(os.getenv("JASID"))):
        if todo == "clear":
            await clearkalender(interact.response)
            return
        if todo == "time":
            await currenttime(interact.response)
            return
        if todo == "show all":
            await showall(interact.response)
            return
        if todo == "daily":
            await called_once_a_day(interact.channel, parse_str_to_ISO_date(debugdate))
            await interact.response.send_message("Done uwu")
            return
        if todo == "altpapier":
            await check_altpapier(interact.channel, debugdate)
            await interact.response.send_message("Done uwu")
    else:
        await interact.response.send_message("Du bist nicht Jas :pleading_face:")

async def clearkalender(channel):
    con = sqlite3.connect(kalender_name) 
    cursor = con.cursor()
    cursor.execute("DELETE FROM event")
    con.commit()
    con.close()
    await channel.send_message(":cactus: Kalender is now empty :cactus:")

async def showall(channel):
    con = sqlite3.connect(kalender_name) 
    cursor = con.cursor()
    res = cursor.execute("SELECT rowid, * FROM event").fetchall()
    con.close()
    await channel.send_message(res)

async def currenttime(channel):
    await channel.send_message(f"{datetime.today()}\nactive at: {str(WHEN)}")


###_BOT_COMMANDS ---------------------------------------------------
@client.tree.command(name="help", description="Gibt Tipps zum Umgang mit dem Bot an.")
async def help(interact: Interaction):
    await interact.response.send_message(":bulb: **Hier ein paar Tipps für den Umgang mit mir :duck:**\n\n*Datumseingabe allgemein:* \nDaten sind im Format `dd.mm.yyyy` einzutragen. Alternativ verstehe ich auch `d.m.yy`  wobei da zu bedenken ist, dass ich davon ausgehe, dass wir und im 21. Jhd. befinden :sweat_smile: \n--> Alternativ dürft ihr auch gerne `heute` bzw. `morgen` als Datum eintragen um Denkzeit zu sparen  uwu\n--> Wochentage sind keine Daten, sry qwq\n\n*Multiple_events:*\n Hier musst du bei Eventnamen und Eventinformationen die einzelnen Events mit einem `;` trennen. Beachte, dass die Anzahl der `;` in beider Feldern gleich sein muss (mit mind einem Leerzeichen dazwischen).\n\n*Eventserie:* \nHier bitte bei `abstand` eine Zahl direkt gefolgt (ohne Leerzeichen) von einem dieser Buchstaben: `d`, `w`, `m` oder `y`. Diese stehen für Tage, Wochen, Monate bzw. Jahre.\n\n*Repeated_events:*\n Hier bitte die Daten mittels Leerzeichen trennen.\n\n*Delete_events:*\n Hier kannst du eine, mehrere oder eine Spanne an IDs angeben in der Form `x`, `x y z`(mit Leerzeichen) oder `x-z`(ohne Leerzeichen) ^^\n\nMit `/help_task` und dann den jeweiligen Tasknamen: `Küche`, `Bad`, `WCs`, `Boden`, `Müll`, `Großputzt` bekommst du Informationen zu den jeweiligen Task. Du musst hier auch nicht auf die Großschreibung achten ^^\n---------------------\n\n*Beispielseingaben:*\n`/single_event datum:01.01.23 eventname:Neu Jahr eventinfo:Ganz laut`\n\n`/multiple_events datum:19.02.23 eventnames:WG-Besprechung; Shisha Abend eventinfos:Mittags; Anna, Emi, Kim`\n\n`/repeated_events eventname:altpapier eventinfo:altpapier rechtzeitig raus dates:16.3.23 13.4.23 4.5.23`\n\n`/eventserie datum:03.02.23 eventname:Film-Friday eventinfo:Dino Nuggets abstand:7d anz_wdh:10`\n\n")    

#-#-#

@client.tree.command(name="task_help", description="Gibt eine Beschreibung zum abgefragten Task an.")
async def task_help(interact: Interaction, task: str):
    task = task.lower()
    if task == "küche":
        await interact.response.send_message(":fork_and_knife: Der **Küchen Task** beinhaltet folgende Aufgaben:\n\n> :white_small_square: Alle Ablagen (auch unter den Geräten) wischen\n> :white_small_square: Wandfließen wischen (vor allem beim Herd)\n> :white_small_square: Überprüfen ob Herd, Ofen und Mikrowelle sauber (ggfs. putzen)\n> :white_small_square: Kaffeemaschine entkalken\n> :white_small_square: Wasserkocher entkalken\n> :white_small_square: Spülbecken mit Essigessenz behandeln (fürs Kellerrohr)\n> Für die Letzten drei Punkte findest du Informationen in #regeln-und-infos uwu")
    elif task == "bad":
        await interact.response.send_message(":bathtub: Der **Bad Task** beinhaltet folgende Aufgaben:\n\n> :white_small_square: Dusche, Badewanne & Waschbecken 1.OG putzen\n> :white_small_square: Dusche im Keller putzen")
    elif task == "wcs" or task == "wc":
        await interact.response.send_message(":toilet: Der **WC Task** beinhaltet folgende Aufgaben:\n\n> :white_small_square: WC im DG, 1.OG sowie EG putzen (Keller nach bedarf)\n> :white_small_square: Überprüfen ob Wasser noch blau ist, wenn nein dann Jas bescheid geben\n> :white_small_square: Die Waschbecken im DG, EG sowie Keller putzen ")
    elif task == "boden":
        await interact.response.send_message(":broom: Der **Boden Task** beinhaltet folgende Aufgaben:\n\n> :white_small_square: Alle Treppen, Flur 1. OG, komplettes EG, sowie Keller saugen\n> :white_small_square: Alle oben genannten Orte nass wischen (muss nicht unbedingt jede Woche sein)\n> Wer freundlich sein will, kann die anderen Mitbewohner fragen, ob diese ihr Zimmer gesaugt haben möchten uwu\n> Diese müssen dann ihr Boden für dich frei machen ^^\n")
    elif task == "müll":
        await interact.response.send_message(":wastebasket: Der **Müll Task** beinhaltet folgende Aufgaben:\n\n> :white_small_square: Müll in der Küchen (Restmüll, Wertstoff & Biomüll) rausbringen\n> :white_small_square: Müll aller WCs rausbringen\n> :white_small_square: Alle Mülleimer wieder mit Müllbeutel ausstatten\n> Wer freundlich sein will, kann die anderen Mitbewohner fragen, ob diese ebenfalls ihren Müll rausgebracht bekommen haben möchten uwu\n")
    elif task == "großputz":
        await interact.response.send_message(":broom:  Der** Großputz** findet jeden **2. Sonntag** des Monats statt. Ausweichtermin ist der  **3. Sonntag** des Monats.\nDabei schauen wir an welche zusaztasks zu erledigen sind.\n**Zusatztasks:** \n> :white_small_square:Staubwischen\n> :white_small_square:Fenster putzen\n> :white_small_square:Fliegennetze\n> :white_small_square:Vorne fegen\n> :white_small_square: Küche-Großputz\n> :white_small_square: Kühlschrank sauber machen\n> :white_small_square:Gartenarbeit\n> :white_small_square: Ausmisten\n")
    else:
        await interact.response.send_message(":x: Bitte gebe eines der folgenden Tasks an um die Beschreibung zu erhalten:\nküche, bad, wcs/wc, boden, müll, großputzt")

#-#-#

@client.tree.command(name = "pet", description="Appreciation für den Haushaltsbot uwu")
async def pet(interact: Interaction):
    user = interact.user
    await interact.response.send_message("Quack quack quack, danke für's streicheln " + user.mention + " ^^\n"
    +"Ich geb mein bestest! Quack :duck::soap:")

#-#-#

@client.tree.command(name = "zuteilung", description="Teilt die Haushaltsaufgaben auf die WG Mitbewohner auf.")
async def zuteilung(interact: Interaction):
    checkmembers(interact.guild)
    global zuteilung
    zuteilung = zuteilen()
    
    await muelldienst(interact.guild)

    home_members.clear()

    await interact.response.send_message("_**Die neue Zuteilung lautet:**_ \n" + zuteilung)

#-#-#

@client.tree.command(name = "single_event", description="Trägt einen einzelnen Termin/Event in den Kalender ein.")
async def single_event(interact: Interaction, datum: str, eventname: str, eventinfo: str):
    _match = re.search(date_regex, datum)
    if _match is None:
        await interact.response.send_message(ungueltiges(datum))

    entrydate = parse_str_to_ISO_date(datum)
    if entrydate < date.today():
        await interact.response.send_message(datum_liegt_in_der_vergangenheit)
    
    global data
    data = []
    new_entry(entrydate, eventname, eventinfo, interact.user.name)
    await interact.response.send_message(insert_into_db(data))

#-#-#

@client.tree.command(name = "multiple_events", description="Trägt mehrere Events für einen Tag ein. Du musst mit | separieren.")
async def multiple_events(interact: Interaction, datum: str, eventnames: str, eventinfos: str):
    global data
    data = []
    _match = re.search(date_regex, datum)
    if _match is None:
        await interact.response.send_message(ungueltiges(datum))
    entrydate = parse_str_to_ISO_date(datum)

    _match = re.search(r"^(?:([\w\d\s.:,\-_+*~#'´`<>()=\][}{&%$\^€\"\"\|!?äöü]+);?)+$", eventnames)
    if _match is None:
        await interact.response.send_message(":x: Bitte nutze ';' als Trennzeichen.")
    names_arr = _match.group(0).split(";")

    _match = re.search(r"^(?:([\w\d\s.:,\-_+*~#'´`<>()=\][}{&%$\^€\"\"\|!?äöü]+);?)+$", eventinfos)
    if _match is None:
        await interact.response.send_message(":x: Bitte nutze ';' als Trennzeichen.")
    infos_arr = _match.group(0).split(";")

    if not len(names_arr) == len(infos_arr):
        await interact.response.send_message(":x: Die Anzahl an Eventnamen und Eventinformationen stimmen nicht überein.")

    for i in range(len(names_arr)):
        new_entry(entrydate, names_arr[i].strip(), infos_arr[i].strip(), interact.user.name)
    await interact.response.send_message(insert_into_db(data))
    
#-#-#

@client.tree.command(name = "repeated_events", description="Trägt eine Serie an gleichen Events, mit unregelmäßigem Abstand, ein.")
async def repeated_events(interact: Interaction, eventname: str, eventinfo: str, dates: str):
    _match = re.search(r"^((?:(?:0[1-9]|[12][0-9]|3[01]|[1-9])\.(?:0[1-9]|1[012]|[1-9])\.(?:20)?\d\d\s?)+)$", dates)
    if _match is None:
        await interact.response.send_message(ungueltiges("Eines der Daten"))
    
    dates = _match.group(0).split()
    global data
    data = []

    for d in dates:
        entrydate = parse_str_to_ISO_date(d)
        if entrydate < date.today():
            await interact.response.send_message(datum_liegt_in_der_vergangenheit)
        new_entry(entrydate, eventname, eventinfo, interact.user.name)
    await interact.response.send_message(insert_into_db(data))

#-#-#

@client.tree.command(name = "eventserie", description="Trägt eine Serie an gleichen Events, mit regelmäßigem Abstand, ein.")
async def eventserie(interact: Interaction, datum: str, eventname: str, eventinfo: str, abstand: str, anz_wdh: int):
    _match = re.search(date_regex, datum)
    if _match is None:
        await interact.response.send_message(ungueltiges(datum))

    entrydate = parse_str_to_ISO_date(datum)
    if entrydate < date.today():
        await interact.response.send_message(datum_liegt_in_der_vergangenheit)
    
    _match = re.search(r"^(0?[1-9]+)([dwmy])$", abstand)
    if _match is None:
        await interact.response.send_message(f":x: Bitte gebe für den Parameter `**abstand**` eine Zahl gefolgt von entweder d, w, m oder y ein.\nd = tage, w = wochen, m = monate, y = jahre.") 

    global data
    data = []
    for i in range(anz_wdh):
        new_entry(add_space(entrydate, int(_match.group(1)), _match.group(2), i), eventname, eventinfo, interact.user.name)
    await interact.response.send_message(insert_into_db(data))

#-#-#

@client.tree.command(name = "add_bday", description="Trägt ein Geburtstag für die nächsten 5 Jahre ein.")
async def add_bday(interact: Interaction, datum: str, name: str):
    _match = re.search(date_regex, datum)
    if _match is None:
        await interact.response.send_message(ungueltiges(datum))

    entrydate = parse_str_to_ISO_date(datum)
    entrydate = date(date.today().year, entrydate.month, entrydate.day)
    global data
    data = []

    for i in range(5):
        new_entry(add_space(entrydate, 1, "y", i), "Geburtstag uwu", name, interact.user.name)
    await interact.response.send_message(insert_into_db(data))

#-#-#

@client.tree.command(name = "abwesenheit", description="Trägt einen Abwesenheits-Eintrag für dich ein.")
async def abwesenheit(interact: Interaction, von_datum: str, bis_datum: str):
    _match = re.search(date_regex, von_datum)
    if _match is None:
        await interact.response.send_message(ungueltiges(von_datum))
    
    _match = re.search(date_regex, bis_datum)
    if _match is None:
        await interact.response.send_message(ungueltiges(bis_datum))
    
    von = parse_str_to_ISO_date(von_datum)
    bis = parse_str_to_ISO_date(bis_datum)

    if von > bis:
        await interact.response.send_message(":x: ungültige Zeitspanne.")
    
    if bis < date.today():
        await interact.response.send_message(datum_liegt_in_der_vergangenheit)

    global data
    data = []

    new_entry(von, "abwesenheit_start", interact.user.id, interact.user.name)
    new_entry(bis, "abwesenheit_ende", interact.user.id, interact.user.name)

    await interact.response.send_message(insert_into_db(data))

#-#-#

@client.tree.command(name = "wochen_uebersicht", description="Gibt auf Befehl eine Wochenübersicht aus.")
async def wochen_uebersicht(interact: Interaction, kalenderwoche: str):
    _match = re.search(r"^((?:(?:[1-4]?[0-9]?)|(?:5[0-2]?))|diese|nächste)$", kalenderwoche)
    if _match is None:
        await interact.response.send_message(":x: Das ist leider keine gültige Kalenderwoche qwq")
    
    week = parse_week_to_ISO(_match.group(1))
    entries = get_entries_of("week", week, date.today().year)
    await interact.response.send_message(create_message_for_entries(entries, f"KW {week}"))

#-#-#

@client.tree.command(name = "monats_uebersicht", description="Gibt auf Befehl eine Monatsübersicht aus.")
async def monats_uebersicht(interact: Interaction, monat: str):
    _match = re.search(r"^([1-9]|1[0-2])$", monat)
    if _match is None:
        await interact.response.send_message(":x: Das ist leider keine gültige Kalenderwoche qwq")
    
    month = int(monat)
    entries = get_entries_of("month", month, date.today().year)
    await interact.response.send_message(create_message_for_entries(entries, f"Monat {month}"))

#-#-#

@client.tree.command(name = "delete_events", description="Löscht das Event bzw Events mit den angegeben IDs.")
async def delete_events(interact: Interaction, ids: str):
    _match = re.search(r"^(\d+)(?:(?:-)(\d+))|(?:(\d+)\s?)+$", ids)
    if _match is None:
        await interact.response.send_message(":x: Bitte gebe eine oder meherere gültige IDs ein. Eingaben werden in der Form `x` `x y z` und `x-z` akzeptiert.")
    
    _match = re.search(r"^(\d+)$", ids)
    if _match is not None:
        id = int(_match.group(1))
        await interact.response.send_message(":scissors: " + delete_from_db(id))
        return
    
    _match = re.search(r"^(?:(\d+)\s?)+$", ids)
    if _match is not None:
        response = ""
        ids_arr = ids.split(" ")
        for id in ids_arr:
            response += delete_from_db(int(id))
        await interact.response.send_message(":scissors: " + response)
        return
    
    _match = re.search(r"^(\d+)(?:(?:-)(\d+))$", ids)
    if _match is not None:
        response = ""
        start = int(_match.group(1))
        end = int(_match.group(2))+1

        for id in range(start, end):
            response += delete_from_db(int(id))
        await interact.response.send_message(":scissors: " + response)
        return
    
    await interact.response.send_message("Idk how we got here")
    

###_DATABASE_INTERACTION ------------------------------------------
def new_entry(eventdate: date, eventname: str, eventinfos: str, author: str):
    global data
    data.append((str(eventdate), str(eventdate.year), str(eventdate.month), str(eventdate.isocalendar()[1]), eventname, eventinfos, author, str(date.today())))
    
def insert_into_db(data):
    con = sqlite3.connect(kalender_name)
    cursor = con.cursor()
    try:
        cursor.executemany("INSERT INTO event VALUES (?, ?, ?, ?, ?, ?, ?, ?)", data)
        con.commit()

        res = cursor.execute("SELECT rowid, date, name, info FROM event ORDER BY rowid DESC").fetchmany(len(data))
        
        if len(res) < 10:
            new_entries = ""
            for entry in res:
                new_entries += f"> **ID:** `{entry[0]}` {parse_date_to_human(entry[1])} {entry[2]} - *{entry[3]}*\n"
        else:
            ids_arr = []
            for entry in res:
                ids_arr.append(entry[0])
            ids_arr.sort()
            new_entries = f"IDs der neuen Einträge: `{ids_arr}`"

        rtr = f":calendar_spiral: Neue/r Eintrag/Einträge erstellt owo\n{new_entries}"
    except:
        rtr = ":x: Eintrag fehlgeschlagen qwq"
    con.close()
    return rtr
    
def delete_from_db(id: int):
    con = sqlite3.connect(kalender_name)
    cursor = con.cursor()
    try:
        cursor.execute(f"DELETE FROM event WHERE rowid={id}")
        con.commit()
        rtr = f"Eintrag mit der ID `{id}` gelöscht\n"
    except:
        rtr = f":x: Löschen vom Eintrag der ID `{id}` fehlgeschlagen qwq\n"
    con.close()
    return rtr

def someone_has_bday(today: date):
    con = sqlite3.connect(kalender_name)
    cursor = con.cursor()
    res = cursor.execute(f"SELECT info FROM event WHERE name='Geburtstag uwu' AND date='{str(today)}'").fetchall()
    con.close()
    return res

async def check_altpapier(channel: discord.TextChannel, today: date):
    tomorrow = datetime.combine(today + timedelta(days=1), time(0)).date()
    con = sqlite3.connect(kalender_name)
    cursor = con.cursor()
    res = cursor.execute(f"SELECT info FROM event WHERE name='altpapier' AND date='{str(tomorrow)}'").fetchall()
    if len(res) > 0:
        await channel.send(f"{line}:newspaper: Altpapier wird **morgen** eingesammelt.\n"
        + f"Denkt daran heute abend es rauszustellen uwu.\n{line}")
    else:
        nextweek = datetime.combine(today + timedelta(days=7), time(0)).date()
        res = cursor.execute(f"SELECT info FROM event WHERE name='altpapier' AND date='{str(nextweek)}'").fetchall()
        if len(res) > 0:
            await channel.send(f"{line}:newspaper: Nächste Woche wird Altpapier eingesammelt ^^\n{line}")
    con.close()

async def check_abwesenheit(today):
    abwesend_role = client.get_guild(guild_id).get_role(abwesend_role_id)

    con = sqlite3.connect(kalender_name)
    cursor = con.cursor()
    res = cursor.execute(f"SELECT info FROM event WHERE name='abwesenheit_start' AND date='{str(today)}'").fetchall()

    if len(res) > 0:
        for entry in res:
            await client.get_guild(guild_id).get_member(entry[0]).add_roles(abwesend_role)
    
    res = cursor.execute(f"SELECT info FROM event WHERE name='abwesenheit_ende' AND date='{str(today)}'").fetchall()
    if len(res) > 0:
        for entry in res:
            await client.get_guild(guild_id).get_member(entry[0]).remove_roles(abwesend_role)
    con.close()

# Get entries of month/week/day = value and year = this year
def get_entries_of(mo_we_da: str, value: str, year: int):
    con = sqlite3.connect(kalender_name)
    cursor = con.cursor()
    res = cursor.execute(f"SELECT date, name, info FROM event WHERE ({mo_we_da}='{value}' AND year='{year}') AND NOT (name='abwesenheit_start' OR name='abwesenheit_ende') ORDER BY date ASC").fetchall()
    con.close()
    return res

def delete_older_then(isoweek: int, year: int):
    con = sqlite3.connect(kalender_name)
    cursor = con.cursor()
    cursor.execute(f"DELETE FROM event WHERE (week < '{isoweek}' AND year = '{year}') OR (week='{isoweek + 51}' AND year = '{year - 1}')")
    con.commit()
    con.close()


###_HELPER_FUNCTIONS_HAUSHALT -----------------------------------------------
# Diese Section wird nochmal überarbeitet
async def neue_zuteilung(channel, today: date):
    guild = client.get_guild(guild_id)
    enddate = datetime.combine(date.today() + timedelta(days=14), time(0)).date()

    checkmembers(guild)
    global zuteilung
    zuteilung = zuteilen()
    await muelldienst(guild)

    home_members.clear()

    await channel.send(f"_**Die neue Zuteilung lautet:**_ \nDiese ist gültig bis zum `{enddate.day}.{enddate.month}.{enddate.year}`\n" + zuteilung)

def checkmembers(guild):   
    global home_members
    role = guild.get_role(member_role_id)
    home_members = role.members

def zuteilen():
    zuteilung = ""
    random.shuffle(tasks)
    i = 0
    for member in home_members:
        if client.get_guild(guild_id).get_role(abwesend_role_id) in member.roles:
            zuteilung += ":island:"
        zuteilung += member.mention + " --> " + tasks[i] + "\n"
        i += 1
        if i == len(tasks):
            break
    return zuteilung

async def muelldienst(guild):    
    global zuteilung
    trackerRole = guild.get_role(trashtracker_role_id)

    lastTrashCollector = trackerRole.members[0]
    await lastTrashCollector.remove_roles(trackerRole)
    i = home_members.index(lastTrashCollector) + 1
    if i >= len(home_members):
        i = 0

    newTrashCollector = home_members[i]
    await newTrashCollector.add_roles(trackerRole)

    zuteilung += "--------------------------\n"
    zuteilung += newTrashCollector.mention + " --> Müll rausbringen"


###_HELPER_FUNCTIONS_KALENDER -----------------------------------------------
def ungueltiges(datum: str):
    return f":x: {datum} ist kein gültiges Datum.\nBitte gebe eine gültiges Datum ein ^^"
    
def parse_str_to_ISO_date(input: str):
    if input == "heute":
        return date.today()
    if input == "morgen":
        return datetime.combine(date.today() + timedelta(days=1), time(0)).date()

    datesplit = input.split(".")
    year = int(datesplit[2])
    if year < 100:
        year += 2000
    return date(year, int(datesplit[1]), int(datesplit[0])) 
    
def parse_date_to_human(input: date):
    datesplit = str(input).split("-")
    return f"{datesplit[2]}.{datesplit[1]}.{datesplit[0]}" 

def parse_week_to_ISO(input):
    if input == "diese":
        return date.today().isocalendar()[1]
    if input == "nächste":
        return date.today().isocalendar()[1] + 1
    return int(input)

def add_space(entrydate: date, space: int, spaceinfo: str, repeat: int):
    nextday = entrydate
    if spaceinfo == "d":
        nextday = datetime.combine(entrydate + timedelta(days=space*repeat), time(0)).date()
    elif spaceinfo == "w":
        nextday = datetime.combine(entrydate + timedelta(weeks=space*repeat), time(0)).date()
    elif spaceinfo == "m":
        nextmonth = nextday.month+space*repeat
        nextyear = nextday.year
        if nextmonth > 12:
            while nextmonth > 12:
                nextmonth = nextmonth - 12
                nextyear += 1
        nextday = date(nextyear, nextmonth, nextday.day)
    elif spaceinfo == "y":
        nextday = date(nextday.year+space*repeat, nextday.month, nextday.day)
    return nextday

def next_Putztag(today: date):
    global guild_id
    role = client.get_guild(guild_id).get_role(member_role_id)
    remainingDays = 7 - today.isoweekday()
    if remainingDays < 0:
        remainingDays = 6
    day1 = today.day + remainingDays + 7
    day2 = day1 + 7

    global data 
    data = []
    new_entry(parse_str_to_ISO_date(f"{day1}.{today.month}.{today.year}"), "Großputztag", "Erster Termin für den monatlichen Großputz", client)
    new_entry(parse_str_to_ISO_date(f"{day2}.{today.month}.{today.year}"), "Großputztag Ausweichtermin", "Ausweichtermin für den monatlichen Großputz", client)
    insert_into_db(data)

    return (f"{line}:broom: {role.mention} Nächster Großputz ist am {day1}.{today.month}.{today.year}\n"
    +f"Ausweichtermin ist am {day2}.{today.month}.{today.year} uwu\n{line}")
    
def birthday_message(bdays):
    message = ""
    for bday in bdays:
        message += f"{line}:birthday: :tada: Quackers, Happy Birthday {bday[0]}!!!\n{line}"
    return message

def create_message_for_entries(entries, scope):
    message = f"{line}:sunny: Guten morgen liebe WG-Menschies, Quack!\n\n"
    if len(entries) > 0:
        message += f"**Termine {scope}:**\n"
        length = 0
        for entry in entries:
            if length < len(entry[1]):
                length = len(entry[1])
        for entry in entries:
            filler = ""
            if length > len(entry[1]):
                for i in range(length - len(entry[1]) + 1):
                    filler += " "
            message += f"`{parse_date_to_human(entry[0])}` {entry[1]}{filler} - *{entry[2]}*\n"
    else:
        message += f"{line}Für {scope} sind *keine* Termine eingetragen.\n"
    return message


###_DAILY_ROUTINE_BACKGROUND --------------------------------------
async def background_task():
    now = datetime.now()
    if now.time() > WHEN:
        tomorrow = datetime.combine(now.date() + timedelta(days=1), time(0))
        seconds = (tomorrow - now).total_seconds()
        await asyncio.sleep(seconds)
        while True:
            now = datetime.now()
            target_time = datetime.combine(now.date(), WHEN)
            seconds_until_target = (target_time - now).total_seconds()
            await asyncio.sleep(seconds_until_target)
            print("it is time to check")
            await called_once_a_day(client.get_channel(output_channel_id), date.today())
            tomorrow = datetime.combine(now.date() + timedelta(days=1), time(0))
            seconds = (tomorrow - now).total_seconds()
            await asyncio.sleep(seconds)

async def called_once_a_day(channel: discord.TextChannel, today: date):
    await client.wait_until_ready()
    thisyear = today.year
    #überprüft ob leute als abwesend eingetragen sind
    await check_abwesenheit(today)
    #if erster Tag des monats? -> Wann nächster Gemeinschaftsputztag
    if today.day == 1:
        message = next_Putztag(today)
        entries = get_entries_of("month", today.month, thisyear)
        await channel.send(create_message_for_entries(entries, "diesen Monat"))
        await channel.send(message)
    #if Montag -> Termine der woche & alte termine löschen
    elif today.isoweekday() == 1:
        thisweek = today.isocalendar()[1]
        if thisweek % 2 == 0:
            await neue_zuteilung(client.get_channel(haushalt_channel_id), today)

        entries = get_entries_of("week", thisweek, thisyear)
        await channel.send(create_message_for_entries(entries, f"diese Woche (KW {thisweek})")+f"\nIch wünsche euch einen angenehmen Start in die Woche :duck:\n{line}")
        delete_older_then(thisweek, thisyear)
    else:
        entries = get_entries_of("date", today, thisyear)
        await channel.send(create_message_for_entries(entries, "heute"))
    #if altpapier in 1 woche -> bescheidgeben
    #if altpapier am nächsten Tag -> erinnern
    await check_altpapier(channel, today)
    #if Freitag -> Blumengießen
    if today.isoweekday() == 5:
        await channel.send(f"{line}:potted_plant: :cup_with_straw: Bitte denk daran die lieben Pflanzen zu gießen uwu\n{line}")
    #if bday -> Gratulieren
    bdays = someone_has_bday(today)
    if len(bdays) > 0:
        message = birthday_message(bdays)
        await channel.send(message)


###_BOT_START -----------------------------------------------------
@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game("Aufräumen"), status=discord.Status.online)
    await client.get_channel(input_channel_id).send(":duck: Quack, Quack, Ich stehe euch zu Diensten :wave:")
    await background_task()

if __name__ == '__main__':
    client.run(os.getenv("TOKEN"))