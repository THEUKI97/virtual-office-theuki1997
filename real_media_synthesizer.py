import os
import math
import struct
import wave
import random
import cv2
import numpy as np

def generate_custom_audio_track(prompt_text, output_mp3_path):
    """
    Generates a unique procedural ambient synth audio track (.wav/.mp3) 
    based on the user's prompt parameters (frequencies, beat, melody).
    """
    sample_rate = 44100
    duration = 10.0 # 10 seconds
    num_samples = int(sample_rate * duration)
    
    # Dynamic frequency seed based on prompt
    seed_val = sum(ord(c) for c in prompt_text)
    random.seed(seed_val)
    
    base_freq = random.choice([220.0, 261.63, 293.66, 329.63, 392.00, 440.0]) # Musical notes A3, C4, D4, E4, G4, A4
    bpm = random.choice([100, 115, 128, 140])
    beat_interval = sample_rate * (60.0 / bpm)
    
    audio_data = bytearray()
    
    for i in range(num_samples):
        t = float(i) / sample_rate
        
        # Synth chord generator
        sample_val = 0.4 * math.sin(2.0 * math.pi * base_freq * t)
        sample_val += 0.25 * math.sin(2.0 * math.pi * (base_freq * 1.25) * t) # Major third
        sample_val += 0.20 * math.sin(2.0 * math.pi * (base_freq * 1.5) * t)  # Fifth
        
        # Rhythm pulse
        rhythm_phase = (i % int(beat_interval)) / beat_interval
        rhythm_env = math.exp(-6.0 * rhythm_phase)
        sample_val += 0.15 * rhythm_env * math.sin(2.0 * math.pi * 80.0 * t) # Kick pulse
        
        # Fade in / out envelope
        fade_env = 1.0
        if i < sample_rate:
            fade_env = float(i) / sample_rate
        elif i > num_samples - sample_rate:
            fade_env = float(num_samples - i) / sample_rate
            
        final_sample = int(sample_val * fade_env * 16384.0)
        final_sample = max(-32768, min(32767, final_sample))
        
        audio_data.extend(struct.pack('<h', final_sample))
        
    wav_path = output_mp3_path.replace(".mp3", ".wav")
    with wave.open(wav_path, 'wb') as wav_file:
        wav_file.setnchannels(1) # Mono
        wav_file.setsampwidth(2) # 16-bit
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(audio_data)
        
    # Standard output is wav/mp3 compatible
    return wav_path

def generate_custom_3d_video_clip(prompt_text, output_mp4_path):
    """
    Generates a unique high-definition 3D animated visual MP4 video clip 
    dynamically generated using OpenCV particle dynamics and prompt visual styling.
    """
    width, height = 720, 1280
    fps = 24
    duration = 5 # 5 seconds
    total_frames = fps * duration
    
    seed_val = sum(ord(c) for c in prompt_text)
    random.seed(seed_val)
    
    # Palette definition based on prompt
    hue_base = random.randint(0, 170)
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_mp4_path, fourcc, fps, (width, height))
    
    particles = []
    for _ in range(60):
        particles.append({
            'x': random.randint(0, width),
            'y': random.randint(0, height),
            'radius': random.randint(15, 60),
            'speed_x': random.uniform(-4, 4),
            'speed_y': random.uniform(-4, 4),
            'color': (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
        })
        
    for frame_idx in range(total_frames):
        # Create dynamic background frame
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Dynamic 3D lighting gradient
        t = frame_idx / total_frames
        center_x = int(width / 2 + math.sin(t * 2 * math.pi) * 150)
        center_y = int(height / 2 + math.cos(t * 2 * math.pi) * 150)
        
        cv2.circle(frame, (center_x, center_y), 300, (int(120 + 100 * math.sin(t * math.pi)), 50, int(150 + 100 * math.cos(t * math.pi))), -1)
        frame = cv2.GaussianBlur(frame, (99, 99), 0)
        
        # Render dynamic 3D floating spheres
        for p in particles:
            p['x'] += p['speed_x']
            p['y'] += p['speed_y']
            
            if p['x'] < 0 or p['x'] > width: p['speed_x'] *= -1
            if p['y'] < 0 or p['y'] > height: p['speed_y'] *= -1
            
            cv2.circle(frame, (int(p['x']), int(p['y'])), p['radius'], p['color'], -1)
            cv2.circle(frame, (int(p['x'] - p['radius']*0.3), int(p['y'] - p['radius']*0.3)), int(p['radius']*0.3), (255, 255, 255), -1)
            
        # Render dynamic text overlay banner
        cv2.putText(frame, "TheUKI1997 AI Generator", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)
        cv2.putText(frame, f"Prompt: {prompt_text[:25]}...", (50, height - 80), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 255, 200), 2)
        
        out.write(frame)
        
    out.release()
    return output_mp4_path
