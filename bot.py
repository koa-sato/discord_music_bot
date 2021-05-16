import discord
import os

from deezer import Deezer

client = discord.Client()
deezer_client = Deezer()

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

@client.event
async def on_message(message):

    # Ignore messages sent by the bot itself to prevent infinite loops
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')
    
    if message.content.startswith('!song'):
        message_arr = message.content.split(" ")
        # If the user didn't input anything after '!song', return an error message
        if len(message_arr) == 1:
            await message.channel.send("Error, no song provided")
            return

        song = " ".join(message_arr[1:])
        await message.channel.send("""Searching for \"""" + str(song) + """\"""")
        url = deezer_client.searchForSong(song)
        if url is None:
            await message.channel.send("Could not find a suitable url for the query")
            return
        await message.channel.send(url)

client.run(os.getenv('TOKEN'))