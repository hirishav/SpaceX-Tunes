import discord
from discord.ext import commands
from utils.music_player import get_queue, music_queues

class Stop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='stop', help='Gaana band karke queue clear karta hai')
    async def stop(self, ctx):
        if ctx.voice_client is not None:
            if ctx.guild.id in music_queues:
                music_queues[ctx.guild.id].clear()
            try:
                if ctx.voice_client.channel:
                    await ctx.voice_client.channel.edit(status=None)
            except:
                pass
            ctx.voice_client.stop()
            await ctx.send(embed=discord.Embed(description="🛑 Sab band! Queue clear kar di hai mene.", color=0xe74c3c))
        else:
            await ctx.send(embed=discord.Embed(description="🤷‍♂️ Lekin me toh kuch baja hi nahi raha!", color=0xff0000))

async def setup(bot):
    await bot.add_cog(Stop(bot))
