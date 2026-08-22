import discord
from discord.ext import commands
import wavelink

class Skip(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='skip', aliases=['s'], help='Current gaana skip karta hai')
    async def skip(self, ctx):
        vc: wavelink.Player = ctx.voice_client
        if vc is not None and vc.playing:
            await vc.skip(force=True)
            await ctx.send(embed=discord.Embed(description="⏭️ Gaana skip kar diya! Next laga raha hu...", color=0xf1c40f))
        else:
            await ctx.send(embed=discord.Embed(description="🤔 Abhi koi gaana nahi chal raha jisko skip karu.", color=0xff0000))

async def setup(bot):
    await bot.add_cog(Skip(bot))
