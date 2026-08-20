import discord
from discord.ext import commands
import os

def is_bot_owner():
    async def predicate(ctx):
        owner_id = os.getenv("OWNER_ID")
        if not owner_id:
            await ctx.send("❌ `OWNER_ID` .env file me set nahi hai!")
            return False
        
        if ctx.author.id == int(owner_id):
            return True
        else:
            await ctx.send("❌ Tum bot ke owner nahi ho bhai! Ye command sirf owner ke liye hai.")
            return False
    return commands.check(predicate)

class OwnerStatus(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='presence', help='Bot ka status change karo (online/idle/dnd/offline) - Only Owner')
    @is_bot_owner()
    async def set_presence(self, ctx, status: str):
        status = status.lower()
        if status == 'online':
            discord_status = discord.Status.online
        elif status == 'idle':
            discord_status = discord.Status.idle
        elif status == 'dnd':
            discord_status = discord.Status.dnd
        elif status in ['offline', 'invisible']:
            discord_status = discord.Status.invisible
        else:
            await ctx.send(embed=discord.Embed(description="❌ Invalid status. Use `online`, `idle`, `dnd`, or `offline`.", color=0xff0000))
            return
            
        # We need to maintain the current activity, otherwise it gets cleared
        current_activity = ctx.me.activity
        await self.bot.change_presence(status=discord_status, activity=current_activity)
        await ctx.send(embed=discord.Embed(description=f"✅ Presence set to **{status}**", color=0x2ecc71))

    @commands.command(name='activity', help='Bot ki activity change karo (playing/watching/listening) - Only Owner')
    @is_bot_owner()
    async def set_activity(self, ctx, act_type: str, *, text: str):
        act_type = act_type.lower()
        if act_type == 'playing':
            activity = discord.Game(name=text)
        elif act_type == 'watching':
            activity = discord.Activity(type=discord.ActivityType.watching, name=text)
        elif act_type == 'listening':
            activity = discord.Activity(type=discord.ActivityType.listening, name=text)
        else:
            await ctx.send(embed=discord.Embed(description="❌ Invalid activity type. Use `playing`, `watching`, or `listening`.", color=0xff0000))
            return

        # We need to maintain the current status
        current_status = ctx.me.status
        await self.bot.change_presence(status=current_status, activity=activity)
        await ctx.send(embed=discord.Embed(description=f"✅ Activity set to **{act_type.capitalize()} {text}**", color=0x2ecc71))

async def setup(bot):
    await bot.add_cog(OwnerStatus(bot))
