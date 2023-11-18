import discord
from discord.ext import commands
import json
import os
from random import choice
from asyncio import sleep
from token_1 import TOKEN

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='cn!', intents=intents)
PATH = "no_context_data.json"
bucle = False

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    synced = await bot.tree.sync()

    
@bot.command(aliases=["p"], description= "ping pong")
async def ping(ctx):
    await ctx.send("pong")
    
    

@bot.command(aliases=["a"], description="add no context")
async def add(ctx: commands.Context, message: str):
    with open(PATH, 'r+', encoding="utf8") as f:
        data = json.load(f)
        data.append(message)
        f.seek(0)
        json.dump(data, f, indent = 4)

        await ctx.send("loaded")


@bot.command(aliases=["s"], description="see no context")
async def see(ctx: commands.Context):
    with open(PATH, 'r', encoding="utf8") as f:
        data_json = json.load(f)
        await ctx.send(choice(data_json))



@bot.tree.command(name="agregar", description="Agrega una frase a sin contexto")
@discord.app_commands.describe(message='mensaje sin contexto')
async def add(interaction: discord.Interaction, message: str):
    with open(PATH, 'r+', encoding="utf8") as f:
        data = json.load(f)
        data.append(message)
        f.seek(0)
        json.dump(data, f, indent = 4)

        await interaction.response.send_message("loaded")

@bot.tree.command(name="ver", description="Muestra una frase sin contexto aleatoria")
async def see(interaction: discord.Interaction):
    with open(PATH, 'r', encoding="utf8") as f:
        data_json = json.load(f)
        await interaction.response.send_message(choice(data_json))

@bot.tree.command(name="fijar_canal", description="Fija el canal para mostrar el sin contexto")
async def canal(interaction: discord.Interaction, channel:discord.TextChannel=None, time: float=None):
    if channel == None:
        channel = interaction.message.channel
    if time == None:
        time = 3600
    bucle = True
    
    await interaction.channel.send("Empezando el bucle")
    while(bucle == True):
        with open(PATH, 'r', encoding="utf8") as f:
            data_json = json.load(f)
            await interaction.channel.send(choice(data_json))
        await sleep(time)

bot.run(TOKEN)