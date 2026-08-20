import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import asyncio
from keep_alive import keep_alive

# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

class SpaceXBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix='!', intents=intents, help_command=None)

    async def setup_hook(self):
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                try:
                    await self.load_extension(f'cogs.{filename[:-3]}')
                    print(f'Loaded Cog: {filename}')
                except Exception as e:
                    print(f'Failed to load {filename}: {e}')

    async def on_ready(self):
        print(f'Launch successful! {self.user.name} is now online and ready for takeoff.')
        await self.change_presence(activity=discord.Game(name="!play | SpaceX Tunes"))

bot = SpaceXBot()

async def main():
    async with bot:
        await bot.start(TOKEN)

if __name__ == '__main__':
    if TOKEN:
        keep_alive()
        asyncio.run(main())
    else:
        print("Error: DISCORD_TOKEN not found in .env file. Please add it and save the file.")
