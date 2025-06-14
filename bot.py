import discord
from dotenv import load_dotenv
import os
from gpt4all import GPT4All
import asyncio

# Load token from .env
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Load the local model
model = GPT4All("mistral.gguf", model_path="./models", allow_download=False)

# Set up Discord bot
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"✅ Logged in as {client.user}!")

'''@client.event
async def on_message(message):
    if message.author == client.user:
        return

    user_input = message.content.strip()

    if user_input.startswith("!"):
        prompt = user_input[1:]
        await message.channel.typing()

        try:
            response = model.generate(prompt, max_tokens=150)
            await message.channel.send(response)
        except Exception as e:
            print(f"❌ Error: {e}")
            await message.channel.send("Sorry, something went wrong.")'''

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    user_input = message.content.strip()

    if user_input.startswith("!"):
        prompt = user_input[1:]
        await message.channel.typing()

        try:
            # Run blocking model.generate in a thread to avoid freezing the event loop
             # 👇 Keeps the typing indicator on while generating response
            async with message.channel.typing():
                response = await asyncio.to_thread(model.generate, prompt, max_tokens=150)
                await message.channel.send(response)
        except Exception as e:
            print(f"❌ Error: {e}")
            await message.channel.send("Sorry, something went wrong.")

client.run(TOKEN)
