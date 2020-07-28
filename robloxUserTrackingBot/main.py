

# |--------------------------------------------------|
# | don't forget to change setting on setting.json   |
# | if you don't change them, bot won't work         |
# |--------------------------------------------------|

# imports
import discord
import json
from discord.ext import commands
from discord.utils import get
import asyncio
from bs4 import BeautifulSoup
import requests

# variables
trackHim = ''
trackYes = True
mentionUser = ''
send2 = ''

# settings variables
with open('settings.json', 'r') as f:
    loaded = json.load(f)
token = loaded['discordBotClientToken']
whoCanUse = loaded['whoCanUseBot']
refresh = loaded['refreshingInterval']
channelToSendTo = loaded['sentTrackingMessagesChannel']
mentionOrNot = loaded['mentionUser']

# bot command prefix
client = commands.Bot(command_prefix='.')


# bot started
@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="command prefix is ."))
    print('bot is running')


# command what will start tracking
@client.command()
async def track(ctx, user):
    global trackHim, trackYes, mentionUser
    trackYes = False
    if whoCanUse == 'everyone':
        trackHim = user
        trackYes = True
        mentionUser = ctx.author.mention
        await ctx.send('tracking started')
        await track2()
    elif str(ctx.message.author) == whoCanUse:
        trackHim = user
        trackYes = True
        mentionUser = ctx.author.mention
        await ctx.send('tracking started')
        await track2()


# stops tracking
@client.command()
async def stoptrack(ctx):
    global trackYes, trackHim
    if whoCanUse == 'everyone':
        trackYes = False
        trackHim = ''
        await ctx.send('tracking stopped')
    elif str(ctx.message.author) == whoCanUse:
        trackYes = False
        trackHim = ''
        await ctx.send('tracking stopped')

# main tracking function
async def track2():
    global send2
    if trackYes:
        channel = client.get_channel(channelToSendTo)
        # gets users profile html file
        result = requests.get(trackHim)
        src = result.content
        soup = BeautifulSoup(src, 'lxml')
        send = ' is offline'
        userText = soup.find('h2', class_='profile-name text-overflow').text
        # find image with user status and changes "send" variable
        if soup.find('span', class_='avatar-status online profile-avatar-status icon-online'):
            send = ' is online'
        elif soup.find('span', class_='avatar-status game icon-game profile-avatar-status'):
            send = ' is gameing'
        elif soup.find('span', class_='avatar-status studio profile-avatar-status icon-studio'):
            send = ' is deving'
        # checks if status isn't the same
        if send != send2:
            if mentionOrNot:
                await channel.send(userText + send + ' ' + mentionUser)
            else:
                await channel.send(userText + send)
        send2 = send
        # waits some time before starting again
        await asyncio.sleep(refresh)
        await track2()

# starts discord bot
client.run(token)
