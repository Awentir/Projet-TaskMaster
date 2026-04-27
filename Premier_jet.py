from discord.ext import commands
from dotenv import load_dotenv
import discord
import os
import aiosqlite

# Permet de charger notre Token
os.getenv("TOKEN")
load_dotenv(dotenv_path="config.txt") 

# Initialisation du bot
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!",intents=intents)

@bot.event
# async def permet de ne pas bloquer le programme pendant que la fonction attend une "action"
async def on_ready():
    async with aiosqlite.connect("taches") as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS globals_tasks(
                id_tache INTEGER PRIMARY KEY,
                id_user INTEGER,
                name TEXT,
                due TEXT,
                priority INTEGER
            )
        """)
        await db.commit() # Très important pour enregistrer les changements !
        print("BDD prête !")
    print(f'Connecté en tant que {bot.user}')

@bot.command(name='close')
async def fermeture(ctx):
    if ctx.author.name == 'awentir':
        bot.close
        print(f'{bot.user} a bien été déconnecté')

@bot.command(name='add')
async def ajout(ctx,name,due,priority):
    async with aiosqlite.connect("taches") as db:
        await db.execute("""
        INSERT INTO globals_tasks (id_user,name,due,priority) VALUES (?,?,?,?);
        """,[ctx.author.id,name,due,priority])

@bot.command(name='suppression')
async def deleteBDD(ctx):
    if ctx.author.id == '352375525282676736':
        async with aiosqlite.connect("taches") as db:
            await db.execute("""
                DROP TABLE globals_tasks
                """)

@bot.command(name='tasks')
async def affiche_tache(ctx):
    tasks_user = discord.Embed(title='*_MES TÂCHES_*',colour=discord.Color.random())
    await ctx.send(embed=tasks_user)



# Token du bot discord
bot.run(os.getenv("TOKEN"))