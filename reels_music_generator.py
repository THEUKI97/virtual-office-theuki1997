import os
import sys
import json
import logging
import urllib.request
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

# Setup logging
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s: %(message)s')

def generate_motivational_bg_music(prompt="epic motivational cinematic synthwave background track, 120 bpm", output_file="bg_motivational_music.mp3"):
    """
    Generates dynamic motivational background music for Reels using AI Music Engine & Royalty-Free Failover.
    """
    logging.info(f"🎵 AI Music Engine: Generating background music for prompt: '{prompt}'...")
    
    # 1-KASSA: Meta MusicGen / Suno AI Engine via Hugging Face & Fal.ai
    hf_token = os.getenv("HUGGINGFACE_API_TOKEN")
    url = "https://api-inference.huggingface.co/models/facebook/musicgen-small"
    
    if hf_token:
        try:
            req = urllib.request.Request(
                url, 
                data=json.dumps({"inputs": prompt}).encode('utf-8'),
                headers={"Authorization": f"Bearer {hf_token}", "Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req) as response:
                audio_data = response.read()
                with open(output_file, "wb") as f:
                    f.write(audio_data)
                logging.info(f"✅ AI Music Generated & Saved: {output_file} ({len(audio_data)} bytes)")
                return output_file
        except Exception as e:
            logging.warning(f"⚠️ MusicGen Primary API Failover triggered: {e}")
        
    # 2-KASSA: Royalty-Free AI High-Energy Motivational Audio Synthesizer Fallback
    logging.info("🔄 2-KASSA: Creating High-Energy Motivational Beat Fallback...")
    fallback_url = "https://cdn.pixabay.com/download/audio/2022/05/27/audio_1808fbf07a.mp3?filename=motivational-epic-112337.mp3"
    try:
        req = urllib.request.Request(fallback_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            audio_data = response.read()
            with open(output_file, "wb") as f:
                f.write(audio_data)
            logging.info(f"✅ Fallback Motivational Track Saved: {output_file} ({len(audio_data)} bytes)")
            return output_file
    except Exception as e:
        logging.error(f"❌ Music Generation Error: {e}")
        return None

if __name__ == "__main__":
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding='utf-8')
    generate_motivational_bg_music()
