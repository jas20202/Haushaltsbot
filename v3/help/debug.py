@client.tree.command(name = "jasdebug", description="Debug Command for Jas")
async def jasdebug(interact: Interaction, todo: str, debugdate: str):
    if(interact.user.id == int(os.getenv("JASBOT_JASID"))):
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