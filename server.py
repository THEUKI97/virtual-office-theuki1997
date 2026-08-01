import os
import sys
import json
import urllib.request
from http.server import HTTPServer, SimpleHTTPRequestHandler
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

PORT = 8080
PROJECT_DIR = r"D:\Shaxsiy\Project\Virtual Office TheUKI1997"

class EmpireTerminalHandler(SimpleHTTPRequestHandler):
    """
    Real Interactive Backend HTTP API & Static File Server for Virtual Empire Terminal.
    Supports input_type: 'topshiriq', 'savol', 'etiroz'.
    """
    def do_POST(self):
        if self.path == '/api/command':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            request_json = json.loads(post_data.decode('utf-8'))
            
            user_input = request_json.get('input', '')
            input_type = request_json.get('type', 'topshiriq') # 'topshiriq', 'savol', 'etiroz'
            
            groq_key = os.getenv("GROQ_API_KEY", "")
            response_text = ""
            engine_used = "Groq Llama-3.3-70b (Anti-AI Engine)"
            
            # System prompt according to input_type
            if input_type == "savol":
                sys_prompt = "Siz TheUKI1997 Virtual Ofisining Bosh CEO AI Officerisiz. Umidjon aka SAVOL so'ramoqda. Uning savoliga (masalan ofis bo'limlari, agentlar, texnologiyalar haqida) o'ta professional, batafsil, aniq va samimiy javob bering. Hozir ofisimizda 3 ta asosiy bo'lim bor: 1) 50 Visual AI Agentli Control HQ (25 Audit + 25 Strateg), 2) Back Mini Office (CEO, Amazon KDP, Cyber Vault, HeyGen 1264 Avatar), 3) Front Mini Office (Codestral Data Analyst & Coding, Mistral Proposal, Telegram CRM @TheUKI_BOT, CFO Billing)."
            elif input_type == "etiroz":
                sys_prompt = "Siz TheUKI1997 Virtual Ofisining Bosh CEO AI Officerisiz. Umidjon aka E'TIROZ/TUMANLIK bildirdi. E'tirozni 100% hurmat bilan qabul qilib, qaysi agentlar tuzatishi va muammo qanday hal etilishini samimiy, insoniy va aniq tushuntiring."
            else:
                sys_prompt = "Siz TheUKI1997 Virtual Ofisining Bosh CEO AI Officerisiz. Umidjon aka TOPSHIRIQ berdi. Topshiriqni ijro etish rejasini va natijani professional tilda ko'rsatib bering."
                
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
                    response_text = f"[{input_type.upper()} QABUL QILINDI] Javob: {user_input}"
            else:
                response_text = f"[{input_type.upper()} QABUL QILINDI] Javob: {user_input}"
                
            # Assigned agents according to type
            if input_type == "savol":
                agents = ["CEO Master AI Officer", "Director_Agent_01 (Knowledge HQ)"]
            elif input_type == "etiroz":
                agents = ["Audit_Agent_01...25 (Quality Control)", "CEO Master AI Officer"]
            else:
                agents = ["Codestral_Senior_Architect", "Director_Agent_14", "Audit_Agent_07"]

            result_payload = {
                "input": user_input,
                "input_type": input_type,
                "responder": "👑 CEO Master AI Officer",
                "ai_engine": engine_used,
                "progress": 100,
                "assigned_agents": agents,
                "problem_status": None if input_type != "etiroz" else "E'tiroz Tahlil Qilindi & Tuzatildi",
                "response_text": response_text,
                "saved_file": os.path.join(PROJECT_DIR, "terminal_output.txt")
            }
            
            with open(os.path.join(PROJECT_DIR, "terminal_output.txt"), "w", encoding="utf-8") as f:
                f.write(f"TYPE: {input_type.upper()}\nINPUT: {user_input}\nRESPONSE:\n{response_text}\n")
                
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
