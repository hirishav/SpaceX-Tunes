import discord
from discord.ext import commands
import wavelink

class Queue(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='queue', aliases=['q'], help='Aage bajne wale gaane dikhata hai')
    async def queue(self, ctx):
        vc: wavelink.Player = ctx.voice_client
        if not vc or vc.queue.is_empty:
            await ctx.send(embed=discord.Embed(description="🗑️ Queue bilkul khali hai bhai! Kuch add toh karo.", color=0xff0000))
            return
        
        embed = discord.Embed(title="🎵 Aage Bajne Wale Gaane", color=0x3498db)
        for idx, track in enumerate(vc.queue, start=1):
            if idx > 10: # Only show first 10
                embed.add_field(name="...", value=f"and {vc.queue.count - 10} more", inline=False)
                break
            embed.add_field(name=f"{idx}.", value=f"**[{track.title}]({track.uri})**", inline=False)
            
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Queue(bot))
