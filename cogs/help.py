import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='help', help='Sare commands ki list dekho')
    async def help_command(self, ctx):
        embed = discord.Embed(
            title="🚀 SpaceX Tunes | Commands Menu",
            description="Ye rahe aapke sabhi music commands! Clickable buttons bhi try karna play me.",
            color=0xff5733 # Rocket Orange/Red
        )
        
        embed.set_thumbnail(url=self.bot.user.display_avatar.url if self.bot.user.display_avatar else None)

        commands_list = [
            ("🎵 `!play <song>`", "Gaana bajao (YouTube/Spotify search ya link)."),
            ("⏸️ `!pause`", "Chal raha gaana rok do."),
            ("▶️ `!resume`", "Ruka hua gaana wapas chalu karo."),
            ("⏭️ `!skip`", "Current gaana hata ke agla lagao."),
            ("⏹️ `!stop`", "Music player band karo aur queue clear karo."),
            ("📜 `!queue`", "Agle aane wale gaano ki list dekho."),
            ("🚀 `!join`", "Bot ko voice channel me bulao."),
            ("👋 `!leave`", "Bot ko channel se bahar nikalo.")
        ]
        
        for name, value in commands_list:
            embed.add_field(name=name, value=value, inline=False)
            
        embed.set_footer(text="Developed by Rishav | SpaceX Tunes")
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Help(bot))
