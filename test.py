import discord
from dotenv import load_dotenv
import os

load_dotenv()  # Load variables from .env file

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True  # Required to receive message content

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"✅ Logged in as {client.user}!")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    user_input = message.content.strip()

    if user_input.startswith("!"):
        prompt = user_input[1:]
        await message.channel.send(f"Echo: {prompt}")

client.run(TOKEN)
