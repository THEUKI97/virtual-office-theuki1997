import os
import sys
import json
import random
import logging
import urllib.request
from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont
from moviepy import ImageClip, AudioFileClip, VideoFileClip

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s: %(message)s')

HUMOROUS_PROMPTS = [
    {
        "title": "Kutilmagan Mushuk Sentiya",
        "prompt": "funny cute cat wearing sunglasses working on laptop, 4k ultra realistic, vibrant cinematic lighting, comedy style",
        "text": "Xo'jayinim ishga ketdi deb o'ylaganda men..."
    },
    {
        "title": "Robot Dasturchi Xatosi",
        "prompt": "funny robot eating pizza while coding on computer, humorous cinematic photo, 4k resolution",
        "text": "Koding 1-urinishdayoq xatosiz ishlaganda..."
    },
    {
        "title": "Aqlli IT Kuchukcha",
        "prompt": "cute puppy wearing business suit reading money charts, funny viral reel, 8k render",
        "text": "Birinchi frilans maoshimni olganimda men..."
    }
]

def generate_viral_humorous_image(prompt_text, output_file="viral_humor.png"):
    """Generates ultra-engaging, funny, human-like visual image using Pollinations AI Engine."""
    logging.info(f"🎨 Generating Funny Visual Image for prompt: '{prompt_text}'...")
    encoded_prompt = urllib.parse.quote(prompt_text)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1080&height=1920&nologo=true&seed={random.randint(1, 99999)}"
    
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as res:
            image_bytes = res.read()
            with open(output_file, "wb") as f:
                f.write(image_bytes)
            logging.info(f"✅ Funny Image Saved: {output_file} ({len(image_bytes)} bytes)")
            return output_file
    except Exception as e:
        logging.error(f"❌ Image generation failed: {e}")
        return None

def add_humorous_text_overlay(image_path, overlay_text, output_file="humor_rendered_frame.png"):
    """Overlays funny human-like text onto the image for viral engagement."""
    img = Image.open(image_path)
    draw = ImageDraw.Draw(img)
    w, h = img.size
    
    try:
        font = ImageFont.truetype("arial.ttf", 52)
    except:
        font = ImageFont.load_default()
        
    # Draw dark semi-transparent banner for text readability
    draw.rectangle([40, h - 350, w - 40, h - 150], fill=(15, 23, 42, 220), outline="#fbbf24", width=4)
    draw.text((w // 2, h - 250), overlay_text, fill="#ffffff", font=font, anchor="mm")
    
    img.save(output_file)
    return output_file

def create_funny_no_voice_reel(concept_item, index=1):
    """Creates a 100% human-like funny Reel with NO AI voice, using dynamic visual + funny background beat."""
    title = concept_item["title"]
    prompt = concept_item["prompt"]
    text = concept_item["text"]
    
    logging.info(f"🚀 Producing Funny Viral Reel #{index}: '{title}'...")
    
    # 1. Generate Funny Visual
    raw_img = generate_viral_humorous_image(prompt, f"raw_humor_{index}.png")
    final_frame = add_humorous_text_overlay(raw_img, text, f"frame_humor_{index}.png")
    
    # 2. Add Funny Upbeat Music Beat (No AI Voice)
    audio_path = "bg_motivational_music.mp3"
    output_mp4 = f"FUNNY_VIRAL_REEL_{index}.mp4"
    
    # 3. Combine into MP4 Video (10 Seconds)
    audio_clip = AudioFileClip(audio_path).subclipped(0, 10)
    video_clip = ImageClip(final_frame).with_duration(10)
    video_clip = video_clip.with_audio(audio_clip)
    
    video_clip.write_videofile(output_mp4, fps=24, codec="libx264", audio_codec="aac", logger=None)
    logging.info(f"🎉 SUCCESS: Funny Viral Reel #{index} Ready: {output_mp4}")
    return output_mp4

if __name__ == "__main__":
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding='utf-8')
        
    for i, item in enumerate(HUMOROUS_PROMPTS, 1):
        create_funny_no_voice_reel(item, i)
