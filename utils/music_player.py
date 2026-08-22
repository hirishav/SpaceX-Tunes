import discord
import yt_dlp
import asyncio
import os
import platform

# Conditional FFmpeg path
if platform.system() == 'Windows':
    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
        'options': '-vn',
        'executable': r'C:\Users\Rishav\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0-full_build\bin\ffmpeg.exe'
    }
else:
    # Linux (Render Docker)
    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
        'options': '-vn',
        'executable': 'ffmpeg'
    }

# Set up yt-dlp options
ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0', # bind to ipv4 since ipv6 addresses cause issues sometimes
    'extractor_args': {
        'youtube': {
            'client': ['android', 'ios', 'tv', 'web']
        }
    }
}

# Resolve absolute path for cookies.txt
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
cookie_path = os.path.join(BASE_DIR, 'cookies.txt')

# Use cookies.txt if it exists to bypass YouTube bot detection
if os.path.exists(cookie_path):
    ytdl_format_options['cookiefile'] = cookie_path
elif platform.system() == 'Windows':
    # Fallback to Chrome/Edge cookies if running locally and no cookies.txt is provided
    ytdl_format_options['cookiesfrombrowser'] = ('chrome',)

ytdl = yt_dlp.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **FFMPEG_OPTIONS), data=data)

# A simple dictionary to keep track of guild queues
music_queues = {}

def get_queue(guild_id):
    if guild_id not in music_queues:
        music_queues[guild_id] = []
    return music_queues[guild_id]
