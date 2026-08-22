import discord
from discord.ext import commands
import wavelink

class Stop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='stop', help='Gaana band karke queue clear karta hai')
    async def stop(self, ctx):
        vc: wavelink.Player = ctx.voice_client
        if vc is not None:
            vc.queue.clear()
            try:
                if vc.channel:
                    await vc.channel.edit(status=None)
            except:
                pass
            await vc.stop()
            await ctx.send(embed=discord.Embed(description="🛑 Sab band! Queue clear kar di hai mene.", color=0xe74c3c))
        else:
            await ctx.send(embed=discord.Embed(description="🤷‍♂️ Lekin me toh kuch baja hi nahi raha!", color=0xff0000))

async def setup(bot):
    await bot.add_cog(Stop(bot))
