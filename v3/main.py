import os
import discord
from dotenv import load_dotenv
from discord import app_commands, Intents, Client, Interaction

from help import helper

'''
Was muss der Bot können?
- Sich bei Discord anmelden
- Kalender verwalten
    - Tägliche Nachricht
    - Wöchentliche Nachricht
    - Monatliche Nachricht
    - Einträge erstellen
    - Einträge Löschen
'''
load_dotenv()

guild_id = int(os.getenv("JASBOT_GUILD"))
# 
member_role_id = int(os.getenv("JASBOT_BIGBRAINTME"))
abwesend_role_id = int(os.getenv("JASBOT_ABWESENDROLLE"))
trashtracker_role_id = int(os.getenv("JASBOT_TRASHTRACKER"))
# 
haushalt_channel_id = int(os.getenv("JASBOT_HAUSHALT"))
input_channel_id = int(os.getenv("JASBOT_INPUT"))
output_channel_id = int(os.getenv("JASBOT_OUTPUT"))
debug_channel_id = int(os.getenv("JASBOT_DEBUG"))
# 
kalender_name = os.getenv("JASBOT_DBNAME")
# 
# data = []
# WHEN = time(6, 0, 0)
# line = "----------\n"
# date_regex = r"^((?:(?:0[1-9]|[12][0-9]|3[01]|[1-9])\.(?:0[1-9]|1[012]|[1-9])\.(?:20)?\d\d)|heute|morgen)$"
# datum_liegt_in_der_vergangenheit = ":question: Dein Datum liegt in der Vergangenheit. Leider kann ich nicht zeireisen :pleading_face:"
# 
# home_members = []
# zuteilung = ""
# tasks = ["Küche", "Bad", "WCs", "Boden"]


class UtilBot(Client):
    def __init__(self, *, intents: Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self) -> None:
        await self.tree.sync()
client = client = UtilBot(intents = discord.Intents.all())

@client.event
async def on_ready():
    # commit = subprocess.check_output(['git', '-C', 'discord/bots/Haushaltsbot', 'rev-parse', '--short', 'HEAD'])

    await client.change_presence(activity=discord.Game("Testen"), status=discord.Status.online)
    print("guild", guild_id)
    print("channel", debug_channel_id)
    print("what is this", client.get_channel(debug_channel_id))
    await client.get_guild(guild_id).get_channel(debug_channel_id).send(f"Lel Test test")

if __name__ == '__main__':
    client.run(os.getenv("JASBOT_TOKEN"))

@client.tree.command(name="help", description="Gibt Tipps zum Umgang mit dem Bot an.")
async def help(interact: Interaction):
    help_message = helper.get_help_message()
    await interact.response.send_message(help_message)

@client.tree.command(name = "pet", description="Appreciation für den Haushaltsbot uwu")
async def pet(interact: Interaction):
    user = interact.user
    await interact.response.send_message("Quack quack quack, danke für's streicheln " + user.mention + " ^^\n"
    +"Ich geb mein bestest! Quack :duck::soap:")