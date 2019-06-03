import feedparser
import discord
import asyncio

url = 'http://blog.counter-strike.net/index.php/feed/'

Client = discord.Client()
global last_id
last_id = []

#---Edit this before running the bot------
#1] Add the App Bot User Token you got from discord here
token = 'ExampleTokenMakeSureItIsEnclosedByQuotes'
#2] Add the Discord Channel IDs to which the bot will message when CSGO updates.
#bot has to be a part of the group to which the channel belongs. duh
channel_id = ['channel1 ID', 'channel2 ID', 'channel3 ID']

async def print_console(text):
    await Client.wait_until_ready()
    print(text)
    for num in channel_id:
        await Client.send_message(Client.get_channel(num),text)

@Client.event
async def on_ready():
    await Client.change_presence(game=discord.Game(name='CSGO-Updates'))
    print('Logged in as')
    print(Client.user.name)
    print(Client.user.id)
    print('------')

@Client.event
async def on_message(message):
    if message.content.startswith('!check'):
        await Client.send_message(message.channel,'bot Running')
    if message.content.startswith('!help'):
        help_msg = '***the currently active commands are:***\n ```css\n{}\n``` \n'
        text = ' !help : displays the help documentation\n !check : checks if the bot is running,returns 0 or no message if bot is having problems\n !madeby : Steam URL of the bot Creator \n '
        await Client.send_message(message.channel, help_msg.format(text))
    if message.content.startswith('!madeby'):
        msg = ' *made by:* \n http://steamcommunity.com/id/zero_aak'
        await Client.send_message(message.channel, msg)

async def main():
    global last_id
    feed = feedparser.parse(url)
    for index in feed.entries:
        last_id.append(index.id)
    print('primary scan complete')
    await print_console('bot started , use !help for help')
    while True:
        await asyncio.sleep(3600)
        feed = feedparser.parse(url)
        for item in feed.entries:
            if item.id not in last_id:
                last_id.append(item.id)
                await print_console(item.link)

Client.loop.create_task(main())
Client.run(token)
