import discord
from discord.ext import commands

class Resume(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='resume', help='Paused gaana wapas chalu karta hai')
    async def resume(self, ctx):
        if ctx.voice_client is not None and ctx.voice_client.is_paused():
            ctx.voice_client.resume()
            await ctx.send(embed=discord.Embed(description="▶️ Gaana wapas chalu ho gaya!", color=0x2ecc71))
        else:
            await ctx.send(embed=discord.Embed(description="🤔 Koi gaana pause pe nahi hai jisko me chalu karu.", color=0xff0000))

async def setup(bot):
    await bot.add_cog(Resume(bot))
