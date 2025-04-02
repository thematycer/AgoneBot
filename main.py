import os
import discord
from dotenv import load_dotenv
from discord.ext import commands

from characterHandler import makeNewChar, getCharInfo



# Load the environment variables
load_dotenv()
token = os.getenv("DISCORD_TOKEN")
prefix = os.getenv("DISCORD_PREFIX", "&")
server_id = os.getenv("DISCORD_SERVER_ID", None)

# Create the client
IntentsMine = discord.Intents.default()
IntentsMine.message_content = True
client = commands.Bot(command_prefix=prefix, intents=IntentsMine)

# what server the commands can be used in, for testing
GUILD_ID = discord.Object(id=server_id)

# start up
@client.event
async def on_ready():
    try:
        commandsSync = await client.tree.sync(guild=GUILD_ID)
        print(f"Synced {len(commandsSync)} commands")
        print(f'{client.user} is running!')
    except Exception as e:
        print(f"Error syncing commands: {e}")


# command handling
@client.tree.command(name="newchar", description="Create new character with specific key", guild=GUILD_ID)
async def newchar(interaction: discord.Interaction, charkey: str):
    makeNewChar(charkey)
    response = getCharInfo(charkey)
    await interaction.response.send_message(response)


@client.tree.command(name="help", description="help command", guild=GUILD_ID)
async def help(interaction: discord.Interaction):
    await interaction.response.send_message("send help message to user")
    await interaction.user.send("this should be a help command")

#entry point
def main():
    client.run(token)

if __name__ == "__main__":
    main()