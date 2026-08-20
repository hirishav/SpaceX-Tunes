import discord
from discord.ext import commands

class Skip(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='skip', aliases=['s'], help='Current gaana skip karta hai')
    async def skip(self, ctx):
        if ctx.voice_client is not None and ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            await ctx.send(embed=discord.Embed(description="⏭️ Gaana skip kar diya! Next laga raha hu...", color=0xf1c40f))
        else:
            await ctx.send(embed=discord.Embed(description="🤔 Abhi koi gaana nahi chal raha jisko skip karu.", color=0xff0000))

async def setup(bot):
    await bot.add_cog(Skip(bot))
