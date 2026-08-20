import discord
from discord.ext import commands
from utils.music_player import YTDLSource, get_queue
from utils.spotify import is_spotify_url, get_track_name
import asyncio

class MusicControls(discord.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=None)
        self.ctx = ctx

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if not self.ctx.voice_client:
            await interaction.response.send_message("Bot abhi kisi channel me nahi hai.", ephemeral=True)
            return False
        if not interaction.user.voice or interaction.user.voice.channel != self.ctx.voice_client.channel:
            await interaction.response.send_message("Bhai pehle bot wale voice channel me toh aao! 🙄", ephemeral=True)
            return False
        return True

    @discord.ui.button(label="Pause", style=discord.ButtonStyle.secondary, emoji="⏸️")
    async def pause_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        vc = self.ctx.voice_client
        if vc and vc.is_playing():
            vc.pause()
            await interaction.response.send_message("⏸️ Music paused.", ephemeral=True)
        else:
            await interaction.response.send_message("Music is not playing.", ephemeral=True)

    @discord.ui.button(label="Resume", style=discord.ButtonStyle.success, emoji="▶️")
    async def resume_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        vc = self.ctx.voice_client
        if vc and vc.is_paused():
            vc.resume()
            await interaction.response.send_message("▶️ Music resumed.", ephemeral=True)
        else:
            await interaction.response.send_message("Music is not paused.", ephemeral=True)

    @discord.ui.button(label="Skip", style=discord.ButtonStyle.primary, emoji="⏭️")
    async def skip_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        vc = self.ctx.voice_client
        if vc and vc.is_playing():
            vc.stop()
            await interaction.response.send_message("⏭️ Skipped current song.", ephemeral=True)
        else:
            await interaction.response.send_message("Nothing to skip.", ephemeral=True)

    @discord.ui.button(label="Stop", style=discord.ButtonStyle.danger, emoji="⏹️")
    async def stop_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        vc = self.ctx.voice_client
        if vc:
            queue = get_queue(self.ctx.guild.id)
            queue.clear()
            vc.stop()
            await interaction.response.send_message("⏹️ Player stopped and queue cleared.", ephemeral=True)
        else:
            await interaction.response.send_message("Not connected.", ephemeral=True)

class Play(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def play_next_async(self, ctx):
        queue = get_queue(ctx.guild.id)
        if len(queue) >= 1:
            song = queue.pop(0)
            ctx.voice_client.play(song['source'], after=lambda e: asyncio.run_coroutine_threadsafe(self.play_next_async(ctx), self.bot.loop))
            
            try:
                await ctx.voice_client.channel.edit(status=f"🎶 {song['title']}")
            except discord.Forbidden:
                pass # Bot might not have permissions
            except Exception:
                pass

            embed = discord.Embed(title="🎶 Now Playing", description=f"**[{song['title']}]({song['url']})**", color=0x00ff00)
            embed.set_footer(text="SpaceX Tunes | Developed by Rishav")
            await ctx.send(embed=embed, view=MusicControls(ctx))
        else:
            try:
                if ctx.voice_client and ctx.voice_client.channel:
                    await ctx.voice_client.channel.edit(status=None)
            except:
                pass
                
            embed = discord.Embed(title="⏹️ Queue Finished", description="Aur gaane daalo bhai! 🎧", color=0xff0000)
            await ctx.send(embed=embed)

    @commands.command(name='play', aliases=['p'], help='Koi bhi gaana bajao (YouTube/Spotify)')
    async def play(self, ctx, *, query: str):
        if not ctx.message.author.voice:
            await ctx.send(embed=discord.Embed(description="Bhai pehle khud toh voice channel me jao! 🙄", color=0xff0000))
            return
        
        channel = ctx.message.author.voice.channel
        
        if ctx.voice_client is None:
            await channel.connect(self_deaf=True)
            # Embed for joining is handled in join.py, but we can just let it be silent here or add a mini embed
        elif ctx.voice_client.channel != channel:
            await ctx.send(embed=discord.Embed(description="Me already dusre channel me hu bhai, waha aa jao.", color=0xff0000))
            return

        async with ctx.typing():
            search_query = query
            if is_spotify_url(query):
                track_name = get_track_name(query)
                if track_name:
                    search_query = track_name
                    await ctx.send(embed=discord.Embed(description=f"Spotify link detect hua! Search kar raha hu: **{search_query}** 🔍", color=0x1db954))
                else:
                    await ctx.send(embed=discord.Embed(description="Yaar is Spotify link me kuch gadbad lag rahi hai ya API set nahi hai. 😅", color=0xff0000))
                    return
            
            if not search_query.startswith('http'):
                search_query = f"ytsearch:{search_query}"

            try:
                player = await YTDLSource.from_url(search_query, loop=self.bot.loop, stream=True)
            except Exception as e:
                await ctx.send(embed=discord.Embed(title="Error", description=f"Error aa gaya bhai gaana dhundne me: ```{e}```", color=0xff0000))
                return

            queue = get_queue(ctx.guild.id)
            queue.append({'source': player, 'title': player.title, 'url': player.url})

            if not ctx.voice_client.is_playing() and not ctx.voice_client.is_paused():
                await self.play_next_async(ctx)
            else:
                embed = discord.Embed(title="📝 Added to Queue", description=f"**[{player.title}]({player.url})**\nPosition: #{len(queue)}", color=0x3498db)
                await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Play(bot))
