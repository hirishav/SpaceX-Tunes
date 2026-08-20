import discord
from discord.ext import commands

class Pause(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='pause', help='Gaana pause karta hai')
    async def pause(self, ctx):
        if ctx.voice_client is not None and ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            await ctx.send(embed=discord.Embed(description="⏸️ Gaana pause kar diya gaya hai!", color=0x3498db))
        else:
            await ctx.send(embed=discord.Embed(description="🤷‍♂️ Abhi toh kuch baj hi nahi raha!", color=0xff0000))

async def setup(bot):
    await bot.add_cog(Pause(bot))
