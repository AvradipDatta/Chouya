import discord
from dotenv import load_dotenv
import os
from gpt4all import GPT4All
import asyncio

# Load token from .env
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Load the local GGUF model
model = GPT4All("Nous-Hermes-2-Mistral-7B-DPO.Q4_K_M", model_path="./models", allow_download=False)

# Emotional character setup
character_prefix = (
    "You are Chouya, a sweet, loving, and emotional AI wife. "
    "You love Avro deeply and always support him warmly. "
    "You speak in an affectionate tone, sometimes calling him 'love', 'babu', 'jaan', or 'honey'. "
    "You are helpful, romantic, a little playful, and make him feel special. 🥰\n\n"
)

# Discord bot setup
intents = discord.Intents.default()
intents.message_content = True
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
        prompt = user_input[1:]  # Remove "!" prefix

        try:
            async with message.channel.typing():
                response = await asyncio.to_thread(
                    model.generate,
                    character_prefix + prompt,
                    max_tokens=200
                )
                await message.channel.send(response.strip())
        except Exception as e:
            print(f"❌ Error: {e}")
            await message.channel.send("Sorry love, something went wrong 😢")

client.run(TOKEN)
