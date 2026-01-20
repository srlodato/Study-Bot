import discord
import os
from dotenv import load_dotenv
from openai import OpenAI

#Load environment variables from .env
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not DISCORD_TOKEN or not OPENAI_API_KEY:
    raise ValueError("Missing DISCORD_TOKEN or OPENAI_API_KEY in .env file")

#OpenAI Client
openai_client = OpenAI(api_key=OPENAI_API_KEY)

#Discord bot intents
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

#Slash command
tree = discord.app_commands.CommandTree(client)

#Bot is ready
@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    await tree.sync()
    print("Bot is ready to run!")

#On receipt of message
@tree.command(name="summarize", description="Summarize text using OpenAI GPT")
async def summarize(interaction: discord.Interaction, *, text: str):
    await interaction.response.defer()
    try:
        #Call OpenAI API
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": text}],
            max_tokens=150
        )
        summary = response.choices[0].message.content.strip()
        await interaction.followup.send(f"**Summary:** {summary}")
    except Exception as e:
        await interaction.followup.send(f"Error summarizing text: {e}")

#Run bot
client.run(DISCORD_TOKEN)


