import discord
from discord.ext import commands
import wavelink

class Autoplay(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='autoplay', aliases=['ap'], help='Toggle auto-playing recommended songs when queue ends')
    async def autoplay(self, ctx):
        if not ctx.voice_client:
            await ctx.send("Bot abhi kisi channel me nahi hai.")
            return
            
        vc: wavelink.Player = ctx.voice_client
        
        # Toggle autoplay mode
        if vc.autoplay == wavelink.AutoPlayMode.enabled:
            vc.autoplay = wavelink.AutoPlayMode.partial
            embed = discord.Embed(title="Autoplay Disabled ❌", description="Ab recommendations khud-ba-khud play nahi honge.", color=0xff0000)
        else:
            vc.autoplay = wavelink.AutoPlayMode.enabled
            embed = discord.Embed(title="Autoplay Enabled ✅", description="Ab gaane khatam hone par similar gaane khud bajne lagenge!", color=0x2ecc71)
            
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Autoplay(bot))
