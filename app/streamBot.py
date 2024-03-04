
import discord
from discord.ext import commands

api_key = 'MTIxNDEwNjA0NjQ2MTkwNjk2NA.GeChRC.69zbzxWARdhoantscV_LzSYMJeeM5eJuN_w8PA'
channel_id = '1193011030100557844'

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

client = discord.Client(intents=intents)

# Variable to store the most recent message
most_recent_message = None

@client.event
async def on_ready():
    #find most recent message
    global most_recent_message
    channel = client.get_channel(int(channel_id))
    messages = await channel.history(limit=1).flatten()
    most_recent_message = f"{messages[0].author.name}: {messages[0].content}"
    print(f'Updated most recent message: {most_recent_message}')
    print(f'Logged in as {client.user}')
    return most_recent_message


@client.event
async def on_message(message):
    global most_recent_message
    if message.author == client.user or str(message.channel.id) != channel_id:
        return

    # Store the message content and author
    most_recent_message = f"{message.author.name}: {message.content}"
    print(f'Updated most recent message: {most_recent_message}')

def get_most_recent_message():
    return most_recent_message

async def start_bot():
    """Async function to start the bot, to be called from main.py."""
    await client.start(api_key)