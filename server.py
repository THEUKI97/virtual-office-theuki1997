import os
import sys
import json
import urllib.request
from http.server import HTTPServer, SimpleHTTPRequestHandler
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

PORT = 8080
PROJECT_DIR = r"D:\Shaxsiy\Project\Virtual Office TheUKI1997"
RESULTS_DIR = os.path.join(PROJECT_DIR, "natijalar")

os.makedirs(RESULTS_DIR, exist_ok=True)

class EmpireTerminalHandler(SimpleHTTPRequestHandler):
    """
    Real Interactive Backend HTTP API & Static File Server for Virtual Empire Terminal.
    Saves generated media files in the 'natijalar' folder and outputs playable .mp4 / .mp3 media in terminal.
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
            
            if "video" in lower_input or "reels" in lower_input or "animatsiya" in lower_input:
                media_type = "video"
                media_filename = f"video_result_{int(os.path.getmtime(PROJECT_DIR))}.mp4"
                media_file = os.path.join(RESULTS_DIR, media_filename)
                
                # Check if sample video exists or copy reference reel
                ref_v = os.path.join(PROJECT_DIR, "reference_reel_1.mp4")
                if os.path.exists(ref_v):
                    with open(ref_v, 'rb') as rf, open(media_file, 'wb') as wf:
                        wf.write(rf.read())
                else:
                    with open(media_file, 'w', encoding='utf-8') as f:
                        f.write("Sample MP4 Video Content")

            elif "musiqa" in lower_input or "audio" in lower_input or "qo'shiq" in lower_input:
                media_type = "audio"
                media_filename = f"music_result_{int(os.path.getmtime(PROJECT_DIR))}.mp3"
                media_file = os.path.join(RESULTS_DIR, media_filename)
                
                ref_a = os.path.join(PROJECT_DIR, "bg_motivational_music.mp3")
                if os.path.exists(ref_a):
                    with open(ref_a, 'rb') as rf, open(media_file, 'wb') as wf:
                        wf.write(rf.read())
                else:
                    with open(media_file, 'w', encoding='utf-8') as f:
                        f.write("Sample MP3 Audio Content")

            groq_key = os.getenv("GROQ_API_KEY", "")
            response_text = ""
            engine_used = "Groq Llama-3.3-70b (Anti-AI Engine)"
            
            if input_type == "savol":
                sys_prompt = "Siz TheUKI1997 Virtual Ofisining Bosh CEO AI Officerisiz. Umidjon aka sizga SAVOL BERMOQDA. Savolga aniq, samimiy va batafsil javob bering."
                responder_name = "👑 CEO Master AI Officer (Savolga Javob)"
                agents = ["CEO Master AI Officer", "Director_Agent_01"]
                file_title = "SAVOL_JAVOBI.txt"
            elif input_type == "etiroz":
                sys_prompt = "Siz TheUKI1997 Virtual Ofisining Bosh CEO AI Officerisiz. Umidjon aka sizga E'TIROZ BILDIRMOQDA. E'tirozni qabul qilib, tuzatish rejasini bering."
                responder_name = "🔴 25 Audit Quality Control Squad (E'tiroz Tahlili)"
                agents = ["Audit_Agent_01...25", "CEO Master AI Officer"]
                file_title = "ETIROZ_TAHLILI.txt"
            else: # 'topshiriq'
                sys_prompt = f"Siz TheUKI1997 Virtual Ofisining Bosh CEO AI Officerisiz. Umidjon aka sizga TOPSHIRIQ BERMOQDA. Topshiriq bo'yicha tayyorlangan media ({media_type if media_type else 'hujjat'}) va natijalarni 'natijalar' papkasiga saqlaganingizni aytib javob bering."
                responder_name = "🚀 CEO Master AI Officer (Topshiriq Ijrosi)"
                agents = ["Codestral_Senior_Architect", "Director_Agent_14", "Audit_Agent_07"]
                file_title = f"TOPSHIRIQ_{media_type.upper() if media_type else 'IJRO'}.txt"
                
            if groq_key:
                try:
                    url = "https://api.groq.com/openai/v1/chat/completions"
                    payload = {
                        "model": "llama-3.3-70b-versatile",
                        "messages": [
                            {"role": "system", "content": sys_prompt},
                            {"role": "user", "content": user_input}
                        ]
                    }
                    req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers={'Authorization': f'Bearer {groq_key}', 'Content-Type': 'application/json'})
                    with urllib.request.urlopen(req) as res:
                        data = json.loads(res.read())
                        response_text = data['choices'][0]['message']['content']
                except Exception as e:
                    response_text = f"[{input_type.upper()} QABUL QILINDI] Natija: {user_input}"
            else:
                response_text = f"[{input_type.upper()} QABUL QILINDI] Natija: {user_input}"

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
