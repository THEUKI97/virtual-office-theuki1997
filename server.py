import os
import sys
import json
import urllib.request
import time
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from dotenv import load_dotenv
from empire_ai_engine import empire_ai
from real_media_synthesizer import generate_custom_audio_track, generate_custom_3d_video_clip

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

PORT = 8080
PROJECT_DIR = r"D:\Shaxsiy\Project\Virtual Office TheUKI1997"
RESULTS_DIR = os.path.join(PROJECT_DIR, "natijalar")

os.makedirs(RESULTS_DIR, exist_ok=True)

class EmpireTerminalHandler(SimpleHTTPRequestHandler):
    """
    Multi-Threaded HTTP API & Static File Server for Virtual Empire Terminal.
    Uses ThreadingHTTPServer so browser requests never freeze or time out.
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
            
            timestamp = int(time.time())
            
            if "video" in lower_input or "reels" in lower_input or "animatsiya" in lower_input or "milo" in lower_input:
                media_type = "video"
                media_filename = f"generated_3d_video_{timestamp}.mp4"
                media_file = os.path.join(RESULTS_DIR, media_filename)
                
                # Real dynamic HD 3D video animation generation
                generate_custom_3d_video_clip(user_input, media_file)

            elif "musiqa" in lower_input or "audio" in lower_input or "qo'shiq" in lower_input:
                media_type = "audio"
                media_filename = f"generated_synth_music_{timestamp}.wav"
                media_file = os.path.join(RESULTS_DIR, media_filename)
                
                # Real dynamic custom synth melody audio generation
                generate_custom_audio_track(user_input, media_file)

            # Generate intelligent response from Empire AI Engine
            response_text = empire_ai.generate_response(user_input, input_type)
            engine_used = "Empire Dynamic AI Media Generator (OpenCV 3D Synth Engine & Multi-Agent HQ)"
            
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
                agents = ["Codestral_Senior_Architect", "Director_Agent_14 (3D Animation Generator)", "Audit_Agent_07"]
                file_title = f"TOPSHIRIQ_{media_type.upper() if media_type else 'IJRO'}_{timestamp}.txt"

            out_file_path = os.path.join(RESULTS_DIR, file_title)
            with open(out_file_path, "w", encoding="utf-8") as f:
                f.write(f"REJIM: {input_type.upper()}\nSAVOL/TOPSHIRIQ: {user_input}\nJAVOB:\n{response_text}\n")
                if media_file:
                    f.write(f"\nYANGI GENERATSIYA QILINGAN FAYL: {media_file}\n")

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
    server = ThreadingHTTPServer(('0.0.0.0', PORT), EmpireTerminalHandler)
    print(f"Empire Multi-Threaded Terminal Server Running at http://127.0.0.1:{PORT} 🟢")
    server.serve_forever()
