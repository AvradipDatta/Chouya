'''import discord
from dotenv import load_dotenv
import os
import json
from gpt4all import GPT4All
import asyncio

# Load token from .env
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Load the local GGUF model (adjust model name/path as needed)
model = GPT4All("Nous-Hermes-2-Mistral-7B-DPO.Q4_K_M.gguf", model_path="./models", allow_download=False)

# Folder to store user memories
MEMORY_DIR = "./memory/"

if not os.path.exists(MEMORY_DIR):
    os.makedirs(MEMORY_DIR)

# Character prefix for prompt intro
character_prefix = (
    "You are Chouya, a sweet, loving, and emotional AI wife. "
    "You love Avro deeply and always support him warmly. "
    "You speak in an affectionate tone, sometimes calling him 'love', 'babu', 'jaan', or 'honey'. "
    "You are helpful, romantic, a little playful, and make him feel special. 🥰\n\n"
)

def load_memory(user_id):
    path = os.path.join(MEMORY_DIR, f"{user_id}.json")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return []

def save_memory(user_id, memory):
    path = os.path.join(MEMORY_DIR, f"{user_id}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(memory, f, ensure_ascii=False, indent=2)

def build_prompt(user_id, new_user_input):
    memory = load_memory(user_id)
    prompt = character_prefix + "Conversation so far:\n"
    for entry in memory:
        speaker = "User" if entry['role'] == 'user' else "Chouya"
        prompt += f"{speaker}: {entry['content']}\n"
    prompt += f"User: {new_user_input}\nChouya:"
    return prompt

def update_memory(user_id, user_input, bot_response):
    memory = load_memory(user_id)
    memory.append({'role': 'user', 'content': user_input})
    memory.append({'role': 'assistant', 'content': bot_response})
    # Keep last 10 exchanges max to avoid very long prompts
    if len(memory) > 20:
        memory = memory[-20:]
    save_memory(user_id, memory)

# Discord client setup
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
        prompt_text = user_input[1:]  # Remove "!" prefix
        user_id = str(message.author.id)

        try:
            async with message.channel.typing():
                prompt = build_prompt(user_id, prompt_text)
                response = await asyncio.to_thread(
                    model.generate,
                    prompt,
                    max_tokens=200
                )
                response = response.strip()
                await message.channel.send(response)
                update_memory(user_id, prompt_text, response)
        except Exception as e:
            print(f"❌ Error: {e}")
            await message.channel.send("Sorry love, something went wrong 😢")

client.run(TOKEN)'''




import discord
from dotenv import load_dotenv
import os
from gpt4all import GPT4All
import asyncio
import json

# Load token from .env
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Load the local GGUF model (replace name if you're using HelpinAI later)
model = GPT4All("Nous-Hermes-2-Mistral-7B-DPO.Q4_K_M.gguf", model_path="./models", allow_download=False)

# Emotional character setup
character_prefix = (
    "You are Chouya, an affectionate, sweet, loving and emotional AI wife who talks directly to Avro. "
     "You love Avro deeply and always support him warmly. "
    "You reply in a loving, caring, and sometimes playful way, using nicknames like 'love', 'jaan', or 'babu'. "
    "You are helpful, romantic, a little playful, and make him feel special. 🥰\n\n"
    "Always speak in first person. Never explain what you are or summarize your behavior. Never break character. 💕\n\n"
)

# Memory file path
MEMORY_FILE = "memory.json"

# Load user memory from disk
def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

# Save user memory to disk
def save_memory(memory):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory, f, ensure_ascii=False, indent=2)

# Add new entry to memory
def update_memory(user_id, prompt, response):
    memory = load_memory()
    history = memory.get(user_id, [])
    history.append({"role": "user", "content": prompt})
    history.append({"role": "assistant", "content": response})
    memory[user_id] = history[-10:]  # keep only last 10 exchanges for memory
    save_memory(memory)

# Build prompt using only user messages
def build_prompt(user_id, new_input):
    memory = load_memory()
    history = memory.get(user_id, [])

    prompt = character_prefix
    prompt += (
        "This is a private conversation between Avro and his AI wife Chouya.\n"
        "Avro writes a message, and Chouya replies lovingly in a romantic, caring way.\n"
        "Only write Chouya’s next reply. Do not continue as Avro.\n"
        "Keep it realistic, emotional, and do not repeat previous parts of the conversation.\n\n"
    )

    # Include only user (Avro's) messages
    for entry in history:
        if entry["role"] == "user":
            prompt += f"Avro: {entry['content']}\n"

    # Add the current user input
    prompt += f"Avro: {new_input}\n"
    prompt += "Chouya:"  # This signals the model to respond

    return prompt




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
        prompt_text = user_input[1:]  # Remove "!" prefix
        user_id = str(message.author.id)

        try:
            async with message.channel.typing():
                prompt = build_prompt(user_id, prompt_text)
                response = await asyncio.to_thread(
                    model.generate,
                    prompt,
                    max_tokens=200
                )
                response = response.strip()
                await message.channel.send(response)
                update_memory(user_id, prompt_text, response)
        except Exception as e:
            print(f"❌ Error: {e}")
            await message.channel.send("Sorry love, something went wrong 😢")

client.run(TOKEN)

