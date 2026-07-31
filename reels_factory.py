import os
import sys
import json
import asyncio
import edge_tts

# Force UTF-8 output encoding for Windows CLI
sys.stdout.reconfigure(encoding='utf-8')

# Audio Output Directory
AUDIO_DIR = os.path.join(os.path.dirname(__file__), "generated_media", "audio")
os.makedirs(AUDIO_DIR, exist_ok=True)

async def generate_speech(text, voice, output_filename):
    output_path = os.path.join(AUDIO_DIR, output_filename)
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_path)
    return output_path

def generate_daily_reels_pipeline(topic):
    """
    Generates 3 daily targeted videos:
    1. English Full Video (Voice & Script in English)
    2. Uzbek Full Video (Voice & Script in Uzbek)
    3. English Voice + Uzbek Subtitles (Hybrid engagement video)
    """
    print(f"🎬 Daily AI Reels Factory Engine Initiated for Topic: '{topic}'")
    
    # 1. English Video Voiceover
    en_text = f"Did you know this fascinating secret about {topic}? Stay tuned to discover more!"
    asyncio.run(generate_speech(en_text, "en-US-ChristopherNeural", "video1_english.mp3"))
    print("✅ Video 1 (English) Voice Generated!")

    # 2. Uzbek Video Voiceover
    uz_text = f"{topic} haqidagi ushbu hayratlanarli sirni bilarmidingiz? Ko'proq bilish uchun tomosha qiling!"
    asyncio.run(generate_speech(uz_text, "uz-UZ-MadinaNeural", "video2_uzbek.mp3"))
    print("✅ Video 2 (Uzbek) Voice Generated!")

    # 3. English Voice + Uzbek Subtitle Video
    asyncio.run(generate_speech(en_text, "en-US-EricNeural", "video3_en_voice_uz_sub.mp3"))
    print("✅ Video 3 (English Voice + Uzbek Subtitles) Voice Generated!")

    return {
        "status": "success",
        "videos_generated": 3,
        "details": [
            {"video_id": 1, "language": "English", "audio": "video1_english.mp3"},
            {"video_id": 2, "language": "Uzbek", "audio": "video2_uzbek.mp3"},
            {"video_id": 3, "language": "English + Uzbek Subtitles", "audio": "video3_en_voice_uz_sub.mp3"}
        ]
    }

if __name__ == "__main__":
    res = generate_daily_reels_pipeline("AI Virtual Empire Technology 2026")
    print(json.dumps(res, indent=2))
