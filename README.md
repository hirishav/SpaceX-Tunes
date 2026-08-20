# 🚀 SpaceX Tunes

**SpaceX Tunes** ek high-performance, modern aur fully-featured Discord Music Bot hai, jo SpaceX ki theme aur rockets se inspire ho ke banaya gaya hai. 
Aapke Discord server pe YouTube aur Spotify ke gaane chalane ka sabse sexy tareeka.

---

## 🔥 Features
- 🎵 **High-Quality Playback:** YouTube aur Spotify URLs (ya search queries) supports karta hai.
- 🎨 **Modern Embed UI:** Sexy aur clean embeds sabhi bot messages ke liye (Join, Play, Skip, Stop).
- 🖱️ **Interactive Buttons:** Gana chalte waqt UI buttons ka maza lo (⏸️ Pause, ▶️ Resume, ⏭️ Skip, ⏹️ Stop) sidhe Discord message par!
- 🎧 **Permanent Deafening:** Bot ko join karte waqt automatically deafen karta hai for better privacy and bandwidth.
- 🚀 **Lag-free Concurrency:** Async aur thread-safe queue architecture ka use karta hai for smooth, gapless playback.
- ✨ **Modular Cogs System:** Ekdam clean, separate command files (`play.py`, `help.py`, `queue.py`, etc.).

---

## 🛠️ Requirements & Setup

### 1. Prerequisites
- **Python 3.10+**
- **FFmpeg:** Installed aur PATH me add hona chahiye (is project me humne FFmpeg ka direct path set kiya hai).
- **Discord Bot Token:** Discord Developer Portal se.

### 2. Installation
Repo clone karo aur dependencies install karo:
```bash
pip install -r requirements.txt
```

### 3. Environment Variables
Ek `.env` file banao aur apna token daalo:
```env
DISCORD_TOKEN=your_token_here
```

### 4. Run the Bot
```bash
python bot.py
```

---

## 📜 Commands Menu (`!help`)
- `!play <song>` – Gaana bajao (YouTube/Spotify search ya link).
- `!pause` – Chal raha gaana rok do.
- `!resume` – Ruka hua gaana wapas chalu karo.
- `!skip` – Current gaana hata ke agla lagao.
- `!stop` – Music player band karo aur queue clear karo.
- `!queue` – Agle aane wale gaano ki list dekho.
- `!join` – Bot ko voice channel me bulao.
- `!leave` – Bot ko channel se bahar nikalo.

---

**Developed by Rishav**  
*To the stars and beyond!* 🌌
