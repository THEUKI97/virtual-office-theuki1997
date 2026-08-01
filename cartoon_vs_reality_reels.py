import os
import sys
import json
import random
import logging
import urllib.request
from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont
from moviepy import ImageClip, AudioFileClip

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s: %(message)s')

# Human Creative Visual Brain: 3D Animated Mascot vs Reality Concepts
CARTOON_VS_REALITY_CONCEPTS = [
    {
        "id": 1,
        "title": "Tungi Ish Tartibi: Multfilm vs Real Hayot",
        "cartoon_prompt": "3d pixar style cute hero character drinking coffee working at neon computer, vibrant 3d animation aesthetic, disney render, masterpiece",
        "reality_prompt": "funny tired cute 3d hero sleeping on keyboard with empty coffee cups around, cute disheveled 3d animation, viral comedy",
        "caption_top": "MULTFILMDA TUNGI ISH:",
        "caption_top_sub": "✨ 1 sekundda daho kod yaratadi va dunyoni qutqaradi!",
        "caption_bottom": "REAL HAYOTDA:",
        "caption_bottom_sub": "😴 03:00 da bitta nuqta vergul (;) qidirib uxlab qoladi!"
    },
    {
        "id": 2,
        "title": "Frilans Boylik: Multfilm vs Real Hayot",
        "cartoon_prompt": "3d pixar style cute hero character swimming in gold coins like scrooge mcduck, 3d animation film style, bright vibrant colors",
        "reality_prompt": "3d pixar style cute hero character carefully counting one dollar bill with magnifying glass, funny 3d animation",
        "caption_top": "MULTFILMDA FRILANSER:",
        "caption_top_sub": "💰 1 ta buyurtma uchun million dollar oladi!",
        "caption_bottom": "REAL HAYOTDA:",
        "caption_bottom_sub": "☕ 5 dollarlik buyurtmani 3 kun bayram qiladi!"
    },
    {
        "id": 3,
        "title": "AI Dasturlash: Multfilm vs Real Hayot",
        "cartoon_prompt": "3d disney pixar style hero snapping fingers and magic ai robot instantly builds futuristic skyscraper city, 3d animation",
        "reality_prompt": "3d pixar style hero character arguing with small cute AI robot pet, funny confused expressions, 3d animation",
        "caption_top": "MULTFILMDA SUN'IY IDROK:",
        "caption_top_sub": "⚡ Bir tugma bilan butun imperiyani quradi!",
        "caption_bottom": "REAL HAYOTDA:",
        "caption_bottom_sub": "🤖 'Ertaga nima yeymiz?' degan savolga 5 daqiqa o'ylanadi!"
    }
]

def generate_3d_pixar_image(prompt_text, output_file):
    """Generates 3D Pixar/Disney style animated hero image."""
    logging.info(f"🎨 Visual Brain: Generating 3D Animated Hero image for: '{prompt_text[:40]}...'")
    encoded_prompt = urllib.parse.quote(prompt_text)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1080&height=960&nologo=true&seed={random.randint(1, 99999)}"
    
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as res:
            image_bytes = res.read()
            with open(output_file, "wb") as f:
                f.write(image_bytes)
            logging.info(f"✅ 3D Hero Render Saved: {output_file} ({len(image_bytes)} bytes)")
            return output_file
    except Exception as e:
        logging.error(f"❌ 3D Render Error: {e}")
        return None

def create_split_screen_cartoon_vs_reality(concept):
    """Creates a side-by-side / top-bottom 1080x1920 split frame comparing Cartoon vs Reality."""
    cid = concept["id"]
    top_img_path = generate_3d_pixar_image(concept["cartoon_prompt"], f"cartoon_top_{cid}.png")
    bot_img_path = generate_3d_pixar_image(concept["reality_prompt"], f"reality_bot_{cid}.png")
    
    w, h = 1080, 1920
    canvas = Image.new('RGB', (w, h), color='#0f172a')
    
    # Open rendered 3D frames
    top_img = Image.open(top_img_path).resize((1080, 860))
    bot_img = Image.open(bot_img_path).resize((1080, 860))
    
    # Paste frames
    canvas.paste(top_img, (0, 80))
    canvas.paste(bot_img, (0, 980))
    
    draw = ImageDraw.Draw(canvas)
    
    # Header Banner
    draw.rectangle([0, 0, w, 80], fill="#6366f1")
    draw.rectangle([0, 940, w, 980], fill="#ec4899")
    
    try:
        font_header = ImageFont.truetype("arial.ttf", 36)
        font_sub = ImageFont.truetype("arial.ttf", 28)
    except:
        font_header = ImageFont.load_default()
        font_sub = ImageFont.load_default()
        
    # Draw Captions
    draw.text((w // 2, 40), concept["caption_top"], fill="#ffffff", font=font_header, anchor="mm")
    draw.text((w // 2, 880), concept["caption_top_sub"], fill="#38bdf8", font=font_sub, anchor="mm")
    
    draw.text((w // 2, 960), concept["caption_bottom"], fill="#ffffff", font=font_header, anchor="mm")
    draw.text((w // 2, 1860), concept["caption_bottom_sub"], fill="#fbbf24", font=font_sub, anchor="mm")
    
    final_frame_path = f"cartoon_vs_reality_frame_{cid}.png"
    canvas.save(final_frame_path)
    return final_frame_path

def render_cartoon_vs_reality_reel(concept):
    """Renders high-engagement 1080x1920 MP4 Video comparing 3D Cartoon Hero vs Reality."""
    cid = concept["id"]
    logging.info(f"🎬 RENDERING 3D CARTOON VS REALITY REEL #{cid}: '{concept['title']}'...")
    
    frame_path = create_split_screen_cartoon_vs_reality(concept)
    audio_path = "bg_motivational_music.mp3"
    output_mp4 = f"CARTOON_VS_REALITY_REEL_{cid}.mp4"
    
    audio_clip = AudioFileClip(audio_path).subclipped(0, 12)
    video_clip = ImageClip(frame_path).with_duration(12)
    video_clip = video_clip.with_audio(audio_clip)
    
    video_clip.write_videofile(output_mp4, fps=24, codec="libx264", audio_codec="aac", logger=None)
    logging.info(f"🎉 SUCCESS: 3D Cartoon vs Reality Reel #{cid} Ready: {output_mp4}")
    return output_mp4

if __name__ == "__main__":
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding='utf-8')
        
    for item in CARTOON_VS_REALITY_CONCEPTS:
        render_cartoon_vs_reality_reel(item)
