import discord
from discord.ext import commands
import wavelink

class Resume(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='resume', help='Paused gaana wapas chalu karta hai')
    async def resume(self, ctx):
        vc: wavelink.Player = ctx.voice_client
        if vc is not None and vc.paused:
            await vc.pause(False)
            await ctx.send(embed=discord.Embed(description="▶️ Gaana wapas chalu ho gaya!", color=0x2ecc71))
        else:
            await ctx.send(embed=discord.Embed(description="🤔 Koi gaana pause pe nahi hai jisko me chalu karu.", color=0xff0000))

async def setup(bot):
    await bot.add_cog(Resume(bot))
