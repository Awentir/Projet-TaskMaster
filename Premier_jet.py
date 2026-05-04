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
                due DATE,
                priority INTEGER
            )
        """)
        await db.commit() # Très important pour enregistrer les changements !
        print("BDD prête !")
    print(f'Connecté en tant que {bot.user}')

@bot.command(name='add')
async def ajout(ctx,name,due,priority):
    async with aiosqlite.connect("taches") as db:
        await db.execute("""
            INSERT INTO globals_tasks (id_user,name,due,priority) VALUES (?,?,?,?);
            """,[ctx.author.id,name,due,priority])
        await db.commit()
        await ctx.send(f"La tache {name} a été ajoutée à votre To-Do List")

@bot.command(name='tasks')
async def affiche_tache(ctx):
    async with aiosqlite.connect("taches") as db:
        tasks="""SELECT * FROM globals_tasks WHERE id_user = ? ORDER BY priority ASC;"""
        datas = await db.execute_fetchall(tasks,[ctx.author.id])
    tasks_user = discord.Embed(title='*_MES TÂCHES_*',colour=discord.Color.random())
    count=0
    for i in datas:
        count+=1
        tasks_user.add_field(name=f"tache {count}",value=f"{i[2]} à faire pour le {i[3]} de priorité {i[4]}", inline=False)
    await ctx.send(embed=tasks_user)

@bot.command(name='suppression')
@commands.has_role(1500761440112480286)
async def deleteBDD(ctx):
    async with aiosqlite.connect("taches") as db:
        await db.execute("""DELETE FROM globals_tasks;""")
        await db.commit()
        await ctx.send("Données supprimées !")  

@bot.command(name='close')
async def fermeture(ctx):
    if ctx.author.id == '352375525282676736':
        bot.close
        print(f'{bot.user} a bien été déconnecté')


# Token du bot discord
bot.run(os.getenv("TOKEN"))