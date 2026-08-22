import discord
from discord.ext import commands
import wavelink
import asyncio
from utils.spotify import is_spotify_url, get_track_name

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
        vc: wavelink.Player = self.ctx.voice_client
        if vc and vc.playing:
            await vc.pause(True)
            await interaction.response.send_message("⏸️ Music paused.", ephemeral=True)
        else:
            await interaction.response.send_message("Music is not playing.", ephemeral=True)

    @discord.ui.button(label="Resume", style=discord.ButtonStyle.success, emoji="▶️")
    async def resume_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        vc: wavelink.Player = self.ctx.voice_client
        if vc and vc.paused:
            await vc.pause(False)
            await interaction.response.send_message("▶️ Music resumed.", ephemeral=True)
        else:
            await interaction.response.send_message("Music is not paused.", ephemeral=True)

    @discord.ui.button(label="Skip", style=discord.ButtonStyle.primary, emoji="⏭️")
    async def skip_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        vc: wavelink.Player = self.ctx.voice_client
        if vc and vc.playing:
            await vc.skip(force=True)
            await interaction.response.send_message("⏭️ Skipped current song.", ephemeral=True)
        else:
            await interaction.response.send_message("Nothing to skip.", ephemeral=True)

    @discord.ui.button(label="Stop", style=discord.ButtonStyle.danger, emoji="⏹️")
    async def stop_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        vc: wavelink.Player = self.ctx.voice_client
        if vc:
            vc.queue.clear()
            await vc.disconnect()
            await interaction.response.send_message("⏹️ Player stopped and queue cleared.", ephemeral=True)
        else:
            await interaction.response.send_message("Not connected.", ephemeral=True)

class Play(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_wavelink_track_start(self, payload: wavelink.TrackStartEventPayload):
        player = payload.player
        if not player:
            return
            
        track = payload.track
        
        try:
            await player.channel.edit(status=f"🎶 {track.title}")
        except discord.Forbidden:
            pass # Bot might not have permissions
        except Exception:
            pass

        if hasattr(player, 'ctx'):
            embed = discord.Embed(title="🎶 Now Playing", description=f"**[{track.title}]({track.uri})**", color=0x00ff00)
            embed.set_footer(text="SpaceX Tunes | Developed by Rishav")
            await player.ctx.send(embed=embed, view=MusicControls(player.ctx))

    @commands.Cog.listener()
    async def on_wavelink_track_end(self, payload: wavelink.TrackEndEventPayload):
        player = payload.player
        if not player:
            return
            
        # Wavelink's AutoPlay handles playing the next track in queue automatically
        # if player.autoplay is set to partial. 
        # But if the queue is empty:
        if player.queue.is_empty:
            try:
                if player.channel:
                    await player.channel.edit(status=None)
            except:
                pass
            
            if hasattr(player, 'ctx'):
                embed = discord.Embed(title="⏹️ Queue Finished", description="Aur gaane daalo bhai! 🎧", color=0xff0000)
                await player.ctx.send(embed=embed)

    @commands.command(name='play', aliases=['p'], help='Koi bhi gaana bajao (YouTube/Spotify)')
    async def play(self, ctx, *, query: str):
        if not ctx.message.author.voice:
            await ctx.send(embed=discord.Embed(description="Bhai pehle khud toh voice channel me jao! 🙄", color=0xff0000))
            return
        
        channel = ctx.message.author.voice.channel
        
        # Connect to voice channel as a wavelink Player
        if not ctx.voice_client:
            vc: wavelink.Player = await channel.connect(cls=wavelink.Player)
            vc.ctx = ctx # Attach ctx for messaging
            vc.autoplay = wavelink.AutoPlayMode.partial # Auto play next from queue
        else:
            vc: wavelink.Player = ctx.voice_client
            vc.ctx = ctx
            if vc.channel != channel:
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

            try:
                tracks = await wavelink.Playable.search(search_query)
                if not tracks:
                    await ctx.send(embed=discord.Embed(description="Bhai ye gaana nahi mila mujhe.", color=0xff0000))
                    return
                
                track = tracks[0] # Get the first result
                
                vc.queue.put(track)
                
                if not vc.playing:
                    # Start playing if not already
                    await vc.play(vc.queue.get())
                else:
                    embed = discord.Embed(title="📝 Added to Queue", description=f"**[{track.title}]({track.uri})**\nPosition: #{vc.queue.count}", color=0x3498db)
                    await ctx.send(embed=embed)
                    
            except Exception as e:
                await ctx.send(embed=discord.Embed(title="Error", description=f"Lavalink Node par error aa gaya: ```{e}```", color=0xff0000))
                return

async def setup(bot):
    await bot.add_cog(Play(bot))
