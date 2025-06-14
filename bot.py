import discord
from dotenv import load_dotenv
import os
from gpt4all import GPT4All
import asyncio

# Load token from .env
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Set up Discord bot with message content intent
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# Load the local model (adjust the name to use Hermes)
model_name = "Nous-Hermes-2-Mistral-7B-DPO.Q4_K_M"  # Change if needed
model_path = "./models"

# Initialize GPT4All model
model = GPT4All(model_name=model_name, model_path=model_path, allow_download=False)

@client.event
async def on_ready():
    print(f"✅ Logged in as {client.user}!")

@client.event
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author == client.user:
        return

    user_input = message.content.strip()

    # Trigger on messages that start with "!"
    if user_input.startswith("!"):
        prompt = user_input[1:].strip()  # Remove the prefix

        try:
            async with message.channel.typing():
                # Run the blocking model.generate in a separate thread
                response = await asyncio.to_thread(model.generate, prompt, max_tokens=150)
                await message.channel.send(response)
        except Exception as e:
            print(f"❌ Error: {e}")
            await message.channel.send("Sorry, something went wrong while generating a response.")

# Run the bot
client.run(TOKEN)
