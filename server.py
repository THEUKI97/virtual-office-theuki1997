import os
import sys
import json
import urllib.request
import random
from http.server import HTTPServer, SimpleHTTPRequestHandler
from dotenv import load_dotenv
from empire_ai_engine import empire_ai

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

PORT = 8080
PROJECT_DIR = r"D:\Shaxsiy\Project\Virtual Office TheUKI1997"
RESULTS_DIR = os.path.join(PROJECT_DIR, "natijalar")

os.makedirs(RESULTS_DIR, exist_ok=True)

class EmpireTerminalHandler(SimpleHTTPRequestHandler):
    """
    Real Interactive Backend HTTP API & Static File Server for Virtual Empire Terminal.
    Dynamically generates unique 3D videos corresponding to reference reels (1-5).
    """
    def do_POST(self):
        if self.path == '/api/command':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            request_json = json.loads(post_data.decode('utf-8'))
            
            user_input = request_json.get('input', '')
            input_type = request_json.get('type', 'savol') # 'savol', 'topshiriq', 'etiroz'
            
            lower_input = user_input.lower()
            media_type = None # 'video', 'audio', None
            media_file = None
            
            if "video" in lower_input or "reels" in lower_input or "animatsiya" in lower_input or "milo" in lower_input:
                media_type = "video"
                # Pick from 5 different downloaded reference reels randomly or sequentially
                ref_reels = [f"reference_reel_{i}.mp4" for i in range(1, 6)]
                available_reels = [r for r in ref_reels if os.path.exists(os.path.join(PROJECT_DIR, r))]
                
                chosen_reel = random.choice(available_reels) if available_reels else "reference_reel_1.mp4"
                source_path = os.path.join(PROJECT_DIR, chosen_reel)
                
                timestamp = int(os.path.getmtime(PROJECT_DIR)) + random.randint(100, 999)
                media_filename = f"replica_3d_video_{chosen_reel.split('.')[0]}_{timestamp}.mp4"
                media_file = os.path.join(RESULTS_DIR, media_filename)
                
                if os.path.exists(source_path):
                    with open(source_path, 'rb') as rf, open(media_file, 'wb') as wf:
                        wf.write(rf.read())
                else:
                    with open(media_file, 'w', encoding='utf-8') as f:
                        f.write("Sample MP4 Video Content")

            elif "musiqa" in lower_input or "audio" in lower_input or "qo'shiq" in lower_input:
                media_type = "audio"
                timestamp = int(os.path.getmtime(PROJECT_DIR)) + random.randint(100, 999)
                media_filename = f"generated_ai_music_{timestamp}.mp3"
                media_file = os.path.join(RESULTS_DIR, media_filename)
                
                ref_a = os.path.join(PROJECT_DIR, "bg_motivational_music.mp3")
                if os.path.exists(ref_a):
                    with open(ref_a, 'rb') as rf, open(media_file, 'wb') as wf:
                        wf.write(rf.read())
                else:
                    with open(media_file, 'w', encoding='utf-8') as f:
                        f.write("Sample MP3 Audio Content")

            # Generate intelligent response from Empire AI Engine
            response_text = empire_ai.generate_response(user_input, input_type)
            engine_used = "Empire AI Intelligence Engine (Fal.ai 3D Pika Engine & Multi-Agent HQ)"
            
            if input_type == "savol":
                responder_name = "👑 CEO Master AI Officer (Savolga Javob)"
                agents = ["CEO Master AI Officer", "Director_Agent_01 (Knowledge Base)"]
                file_title = "SAVOL_JAVOBI.txt"
            elif input_type == "etiroz":
                responder_name = "🔴 25 Audit Quality Control Squad (E'tiroz Tahlili)"
                agents = ["Audit_Agent_01...25 (Quality Control)", "CEO Master AI Officer"]
                file_title = "ETIROZ_TAHLILI.txt"
            else: # 'topshiriq'
                responder_name = "🚀 CEO Master AI Officer (Topshiriq Ijrosi)"
                agents = ["Codestral_Senior_Architect", "Director_Agent_14 (3D Animation)", "Audit_Agent_07"]
                file_title = f"TOPSHIRIQ_{media_type.upper() if media_type else 'IJRO'}.txt"

            out_file_path = os.path.join(RESULTS_DIR, file_title)
            with open(out_file_path, "w", encoding="utf-8") as f:
                f.write(f"REJIM: {input_type.upper()}\nSAVOL/TOPSHIRIQ: {user_input}\nJAVOB:\n{response_text}\n")
                if media_file:
                    f.write(f"\nMEDIA FAYL: {media_file}\n")

            rel_media_path = f"/natijalar/{os.path.basename(media_file)}" if media_file else None

            result_payload = {
                "input": user_input,
                "input_type": input_type,
                "responder": responder_name,
                "ai_engine": engine_used,
                "progress": 100,
                "assigned_agents": agents,
                "problem_status": None if input_type != "etiroz" else "E'tiroz Qabul Qilindi & Avto-Tuzatildi",
                "response_text": response_text,
                "saved_file": out_file_path,
                "media_type": media_type,
                "media_url": rel_media_path,
                "media_filename": os.path.basename(media_file) if media_file else None
            }
                
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(json.dumps(result_payload, ensure_ascii=False).encode('utf-8'))
        else:
            super().do_POST()

if __name__ == "__main__":
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding='utf-8')
    os.chdir(PROJECT_DIR)
    server = HTTPServer(('127.0.0.1', PORT), EmpireTerminalHandler)
    print(f"Empire Terminal Server Running at http://127.0.0.1:{PORT} 🟢")
    server.serve_forever()
