import os
import sys
import asyncio
import logging
import edge_tts
from reels_music_generator import generate_motivational_bg_music

# Setup logging
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s: %(message)s')

# Voice configuration: 100% Free Edge-TTS natural neural voices
VOICE_EN = "en-US-ChristopherNeural"  # High energy English male voice
VOICE_UZ = "uz-UZ-MadinaNeural"       # Natural Uzbek female voice

async def create_speech(text, voice, output_filename):
    """Generate high-quality TTS audio file."""
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_filename)
    logging.info(f"✅ Audio generated: {output_filename}")

async def main():
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding='utf-8')
        
    logging.info("🚀 REELS FACTORY: Starting Daily 3-Video Audio & Motivational Music Engine...")

    # 1. Video 1: 100% English (Motivation & Tech Trends)
    prompt_video1 = "Did you know that autonomous AI agents are revolutionizing web development in 2026? Build your future empire today with smart AI workflows!"
    await create_speech(prompt_video1, VOICE_EN, "video1_english.mp3")

    # 2. Video 2: 100% Uzbek (Qiziqarli Motivatsion Kontent)
    prompt_video2 = "Sun'iy idrok va avtonom botlar 2026 yilda barcha bizneslarni tubdan o'zgartirmoqda. O'z raqamli imperiyangizni bugun qurishni boshlang!"
    await create_speech(prompt_video2, VOICE_UZ, "video2_uzbek.mp3")

    # 3. Video 3: English Voice + Uzbek Subtitles (Hybrid Engagement)
    prompt_video3 = "Success belongs to those who adapt to artificial intelligence fastest. Automate your work, dominate the market, and scale infinitely!"
    await create_speech(prompt_video3, VOICE_EN, "video3_en_voice_uz_sub.mp3")

    # 4. Generate Motivational AI Background Music Track
    bg_music = generate_motivational_bg_music("epic motivational cinematic synthwave background track, 120 bpm", "bg_motivational_music.mp3")

    logging.info("🎉 SUCCESS: All 3 Daily Reels Audios + AI Motivational Music Track are ready!")
    logging.info("📁 Output Files: video1_english.mp3, video2_uzbek.mp3, video3_en_voice_uz_sub.mp3, bg_motivational_music.mp3")

if __name__ == "__main__":
    asyncio.run(main())
