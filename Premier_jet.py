import discord
from dotenv import load_dotenv
import os

# Permet de charger notre Token
os.getenv("TOKEN")
load_dotenv(dotenv_path="config.txt") 

# Initialisation du bot
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
# async def permet de ne pas bloquer le programme pendant que la fonction attend une "action"
async def on_ready():
    print(f'Connecté en tant que {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        # Await est essentiel, il permet qu'en attendant la permission de Discord pour envoyer le message de faire autre chose, il n'est donc pas gelé.
        await message.channel.send('Hello!')
    
    if message.author.name == 'awentir':
        if message.content == '!close':
            print(f'{client.user} a bien été déconnecté')
            client.close

# Token du bot discord
client.run(os.getenv("TOKEN"))