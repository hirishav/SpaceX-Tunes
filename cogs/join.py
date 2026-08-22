import discord
from discord.ext import commands
import wavelink

class Join(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='join', help='Bot ko voice channel me bulata hai')
    async def join(self, ctx):
        if not ctx.message.author.voice:
            await ctx.send("Bhai pehle khud toh voice channel me jao! 🙄")
            return
        
        channel = ctx.message.author.voice.channel
        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)
        
        await channel.connect(cls=wavelink.Player, self_deaf=True)
        embed = discord.Embed(description=f"🚀 Lo aa gaya me **{channel}** me!", color=0x2ecc71)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Join(bot))
