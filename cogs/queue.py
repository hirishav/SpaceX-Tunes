import discord
from discord.ext import commands
from utils.music_player import get_queue

class Queue(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='queue', aliases=['q'], help='Aage bajne wale gaane dikhata hai')
    async def queue(self, ctx):
        queue = get_queue(ctx.guild.id)
        if not queue:
            await ctx.send(embed=discord.Embed(description="🗑️ Queue bilkul khali hai bhai! Kuch add toh karo.", color=0xff0000))
            return
        
        embed = discord.Embed(title="🎵 Aage Bajne Wale Gaane", color=0x3498db)
        for idx, song in enumerate(queue, start=1):
            embed.add_field(name=f"{idx}.", value=f"**[{song['title']}]({song['url']})**", inline=False)
            
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Queue(bot))
