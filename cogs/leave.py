import discord
from discord.ext import commands
from utils.music_player import music_queues

class Leave(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='leave', aliases=['disconnect', 'dc'], help='Bot ko voice channel se bahar nikalta hai')
    async def leave(self, ctx):
        if ctx.voice_client is not None:
            try:
                if ctx.voice_client.channel:
                    await ctx.voice_client.channel.edit(status=None)
            except:
                pass
            await ctx.voice_client.disconnect()
            if ctx.guild.id in music_queues:
                music_queues[ctx.guild.id].clear()
            await ctx.send(embed=discord.Embed(description="👋 Chalo me chalta hu, fir milenge!", color=0x9b59b6))
        else:
            await ctx.send(embed=discord.Embed(description="🤔 Me toh kisi voice channel me hu hi nahi!", color=0xff0000))

async def setup(bot):
    await bot.add_cog(Leave(bot))
