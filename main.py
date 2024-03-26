import nextcord
from nextcord.ext import commands
import os
from openai import OpenAI, AsyncOpenAI
from constants import OPENAI_TOKEN, BOT_TOKEN, GPT_CHANNEL_ID

client = AsyncOpenAI(
    api_key=OPENAI_TOKEN,
)

class Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def on_ready(self):
        print("Ready!")
    
    async def on_message(self, message):
        if message.channel.id == GPT_CHANNEL_ID and not message.author.bot:
            msg = await message.reply("Generating content...")
            chat_completion = await client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": message.content
                    }
                ],
                model="gpt-4-1106-preview",
            )
            embed = nextcord.Embed(description=chat_completion.choices[0].message.content)
            await msg.edit(content="", embed=embed)


intents = nextcord.Intents.all()
intents.message_content = True
bot = Bot(command_prefix="!", intents=intents)

bot.run(BOT_TOKEN)