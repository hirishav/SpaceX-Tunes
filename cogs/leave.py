import discord
from discord.ext import commands
import wavelink

class Leave(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='leave', aliases=['disconnect', 'dc'], help='Bot ko voice channel se bahar nikalta hai')
    async def leave(self, ctx):
        vc: wavelink.Player = ctx.voice_client
        if vc is not None:
            try:
                if vc.channel:
                    await vc.channel.edit(status=None)
            except:
                pass
            vc.queue.clear()
            await vc.disconnect()
            await ctx.send(embed=discord.Embed(description="👋 Chalo me chalta hu, fir milenge!", color=0x9b59b6))
        else:
            await ctx.send(embed=discord.Embed(description="🤔 Me toh kisi voice channel me hu hi nahi!", color=0xff0000))

async def setup(bot):
    await bot.add_cog(Leave(bot))
