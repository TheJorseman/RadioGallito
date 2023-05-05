import discord
import csv
import os
from discord.ext import commands
from discord.utils import get
from dotenv import load_dotenv

load_dotenv()

#TOKEN = 'MTEwMjc2MDA4MzE3MzE1OTAzMw.GOMljQ.OW1VDDjMH-L4LamznElEBnn7cqhaoPgq4bKm-o'
TOKEN = os.getenv('DISCORD_BOT_TOKEN')
RADIO_FILE = 'radio.csv'

intents = discord.Intents().all()
bot = commands.Bot(command_prefix='!', intents=intents)

radio_stations = []
def cargar_estaciones():
    """Función para cargar la lista de estaciones de radio desde un archivo CSV."""
    with open(RADIO_FILE, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            radio_stations.append({'url': row[0], 'name': row[1], 'genere': row[2], 'country': row[3]})

@bot.command()
async def list(ctx):
    """Comando para listar las estaciones de radio disponibles."""
    response = "Estaciones de radio disponibles:\n\n"
    for station in radio_stations:
        response += f"{station['name']} - {station['genere']}\n"
    await ctx.send(response)

@bot.event
async def on_ready():
    cargar_estaciones()
    print('Music Bot Ready')

@bot.command(pass_context=True)
async def radio(ctx, *, name):
    """Reproduce una estación de radio en el canal de voz actual."""
    channel = ctx.message.author.voice.channel
    url = ''
    if not name.startswith('http'):
        for station in radio_stations:
            if name.lower() in station['name'].lower():
                url = station['url']
                break
    else:
        url = name
    global player
    try:
        player = await channel.connect()
    except:
        pass
    player.play(discord.FFmpegPCMAudio(url))

# No jala, hay que checar una forma de modificar el volumen
# Hay un modulador en la documentacion de discord pero ya no investigue mas xd

@bot.command(pass_context=True)
async def volumen(ctx, volume: float):
    """Comando para ajustar el volumen del reproductor de audio."""
    #voice = get(bot.voice_clients, guild=ctx.guild)
    if player and player.is_playing():
        player.volume = volume
        await ctx.send(f'Volumen ajustado a {int(volume)}%')
    else:
        await ctx.send('No estoy reproduciendo nada en este momento')

@bot.command(aliases=['s', 'sto'])
async def stop(ctx):
    await ctx.send('No estoy reproduciendo nada en este momento')
    player.stop()


bot.run(TOKEN)
