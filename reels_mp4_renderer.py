import os
import sys
import logging
import urllib.request
from PIL import Image, ImageDraw, ImageFont

# Setup logging
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s: %(message)s')

def create_reels_visual_cover(text_title, output_image_path="reels_cover.png"):
    """Creates a high-definition 1080x1920 vertical visual frame for Reels."""
    width, height = 1080, 1920
    img = Image.new('RGB', (width, height), color='#0f172a')
    draw = ImageDraw.Draw(img)
    
    # Draw background gradient aesthetic
    for y in range(height):
        r = int(15 + (y / height) * 30)
        g = int(23 + (y / height) * 40)
        b = int(42 + (y / height) * 80)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
        
    # Draw decorative AI neon border
    draw.rectangle([40, 40, width - 40, height - 40], outline="#6366f1", width=8)
    draw.rectangle([60, 60, width - 60, height - 60], outline="#38bdf8", width=4)
    
    # Add Title Header
    try:
        font_large = ImageFont.truetype("arial.ttf", 64)
        font_sub = ImageFont.truetype("arial.ttf", 44)
    except:
        font_large = ImageFont.load_default()
        font_sub = ImageFont.load_default()
        
    draw.text((width // 2, 350), "THEUKI1997 AI EMPIRE", fill="#f59e0b", font=font_large, anchor="mm")
    draw.text((width // 2, 450), text_title, fill="#ffffff", font=font_sub, anchor="mm")
    draw.text((width // 2, 1600), "🔥 2026 Autonomous AI Reels", fill="#38bdf8", font=font_sub, anchor="mm")
    
    img.save(output_image_path)
    logging.info(f"✅ Visual Frame Rendered: {output_image_path}")
    return output_image_path

def render_mp4_video(audio_file, title, output_mp4):
    """Renders full MP4 video file merging visual frame + speech audio."""
    logging.info(f"🎬 RENDERING FULL MP4 VIDEO: {output_mp4}...")
    try:
        from moviepy import ImageClip, AudioFileClip
        
        # 1. Create HD Visual Frame
        cover_img = create_reels_visual_cover(title, f"cover_{output_mp4}.png")
        
        # 2. Load Audio Clip
        audio_clip = AudioFileClip(audio_file)
        duration = audio_clip.duration
        
        # 3. Combine Image + Audio into MP4
        video_clip = ImageClip(cover_img).with_duration(duration)
        video_clip = video_clip.with_audio(audio_clip)
        
        # 4. Write MP4 File
        video_clip.write_videofile(
            output_mp4, 
            fps=24, 
            codec="libx264", 
            audio_codec="aac",
            logger=None
        )
        logging.info(f"🎉 SUCCESS: Full MP4 Video Saved: {output_mp4} (Duration: {duration:.1f}s)")
        return output_mp4
    except Exception as e:
        logging.error(f"❌ MP4 Rendering Error for {output_mp4}: {e}")
        return None

if __name__ == "__main__":
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding='utf-8')
        
    render_mp4_video("video1_english.mp3", "Autonomous AI Agents 2026", "REELS_1_ENGLISH.mp4")
    render_mp4_video("video2_uzbek.mp3", "Sun'iy Idrok Imperiyasi", "REELS_2_UZBEK.mp4")
    render_mp4_video("video3_en_voice_uz_sub.mp3", "Success & AI Automation", "REELS_3_HYBRID.mp4")
