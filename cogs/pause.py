import discord
from discord.ext import commands
import wavelink

class Pause(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='pause', help='Gaana pause karta hai')
    async def pause(self, ctx):
        vc: wavelink.Player = ctx.voice_client
        if vc is not None and vc.playing:
            await vc.pause(True)
            await ctx.send(embed=discord.Embed(description="⏸️ Gaana pause kar diya gaya hai!", color=0x3498db))
        else:
            await ctx.send(embed=discord.Embed(description="🤷‍♂️ Abhi toh kuch baj hi nahi raha ya already paused hai!", color=0xff0000))

async def setup(bot):
    await bot.add_cog(Pause(bot))
