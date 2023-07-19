import discord
import responses
import json
from os.path import exists

async def send_message(message, movies, username, user_message, is_private):
    try:
        response = responses.get_response(user_message, movies, username)
        await message.author.send(response) if is_private else await message.channel.send(response)
        f = open("movies.json", "w+")
        json.dump(movies, f, indent=4)
        f.close()

    except Exception as e:
        print(e)

def run_discord_bot():
    keys_file  = open("info.txt", "r")
    token = ""
    for line in keys_file:
        sp = line.split(" = ", 1)
        if("TOKEN" in sp[0]):
            token = sp[1]
            break

    movies = dict() #movies={wl: {nome: imdb_link}, sl : {nome_filme: rating} }
    if(exists("movies.json")):
        with open("movies.json", "r") as f:
            movies = json.load(f)
            print("aberto", movies)
            f.close()
    else:
        movies["wl"] = dict()
        movies["sl"] = dict()
        f = open("movies.json", "w+")
        json.dump(movies, f, indent=4)
        f.close()
        print("aberto", movies)

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

        print(f'{username} said: "{user_message}" ({channel})')

        if user_message[0:2] == 'p!':
            user_message = user_message[1:]
            await send_message(message, movies, username, user_message, is_private=True)
        elif user_message[0] == '!':
            await send_message(message, movies, username, user_message, is_private=False)

    client.run(token)