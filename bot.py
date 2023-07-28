import discord
import responses
import json
from mov import movie
from dotenv import load_dotenv
from os import getenv

async def send_message(message, movie_db: movie, username, user_message, is_private, restrict=None):
    try:
        response = responses.get_response(user_message, movie_db, username, restrict)
        movie_db.close()
        await message.author.send(response) if is_private else await message.channel.send(response)

    except Exception as e:
        print(e)

def run_discord_bot():
    # Loading the discord token
    load_dotenv()
    TOKEN = getenv("TOKEN")

    movie_db = movie()

    intents = discord.Intents.default()
    intents.message_content = True

    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'{client.user} is now running')

    @client.event
    async def on_message(message):
        
        if message.author == client.user:
            return
        
        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        if(not (user_message[0:2] == 'p!' or user_message[0:3] == 'ps!' or user_message[0:3] == 'sp!' or user_message[0] == '!' or user_message[0:2] == 's!')):
            return 

        print(f'{username} said: "{user_message}" ({channel})')

        movie_db.connect()

        userInfo = movie_db.checkUser(username)

        movie_db.close()

        if(userInfo.get("banned")):
            await message.channel.send("You have been banned")
            return

        restrict = not userInfo.get("permission")

        if user_message[0:2] == 'p!':
            user_message = user_message[1:]
            await send_message(message, movie_db, "server", user_message, is_private=True, restrict=restrict)
        if user_message[0:3] == 'ps!' or user_message[0:3] == 'sp!':
            user_message = user_message[2:]
            await send_message(message, movie_db, username, user_message, is_private=True)
        elif user_message[0] == '!':
            await send_message(message, movie_db, "server", user_message, is_private=False, restrict=restrict)
        elif user_message[0:2] == 's!':
            user_message = user_message[1:]
            await send_message(message, movie_db, username, user_message, is_private=False)


    client.run(TOKEN)