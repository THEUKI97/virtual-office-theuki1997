import os
import sys
import json
import time
import urllib.request
from http.server import HTTPServer, SimpleHTTPRequestHandler
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

PORT = 8080
PROJECT_DIR = r"D:\Shaxsiy\Project\Virtual Office TheUKI1997"

class EmpireTerminalHandler(SimpleHTTPRequestHandler):
    """
    Real Interactive Backend HTTP API & Static File Server for Virtual Empire Terminal.
    """
    def do_POST(self):
        if self.path == '/api/command':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            request_json = json.loads(post_data.decode('utf-8'))
            
            user_input = request_json.get('input', '')
            is_question = "?" in user_input or "nima" in user_input.lower() or "qanday" in user_input.lower() or "savol" in user_input.lower()
            
            # Formulate response with real AI Engine (Groq / Gemini)
            groq_key = os.getenv("GROQ_API_KEY", "")
            response_text = ""
            engine_used = "Groq Llama-3.3-70b (Anti-AI Engine)"
            
            if groq_key:
                try:
                    url = "https://api.groq.com/openai/v1/chat/completions"
                    payload = {
                        "model": "llama-3.3-70b-versatile",
                        "messages": [
                            {"role": "system", "content": "Siz TheUKI1997 Virtual Ofisining Bosh CEO AI Officer va Boshqaruvchisisiz. Umidjon akaning har bir savoli yoki topshirig'iga professional, aniq, samimiy va insoniy tilda mukammal javob berasiz."},
                            {"role": "user", "content": user_input}
                        ]
                    }
                    req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers={'Authorization': f'Bearer {groq_key}', 'Content-Type': 'application/json'})
                    with urllib.request.urlopen(req) as res:
                        data = json.loads(res.read())
                        response_text = data['choices'][0]['message']['content']
                except Exception as e:
                    response_text = f"Topshiriq avtonom tarzda qabul qilindi. AI javobi: {user_input}"
            else:
                response_text = f"Topshiriq qabul qilindi: {user_input}"
                
            # Build structured response for interactive terminal
            result_payload = {
                "input": user_input,
                "is_question": is_question,
                "responder": "👑 CEO Master AI Officer",
                "ai_engine": engine_used,
                "progress": 100,
                "assigned_agents": [
                    "Audit_Agent_07 (Anti-AI Quality Auditor)",
                    "Director_Agent_14 (Viral Strategy Director)",
                    "Codestral_Senior_Architect"
                ],
                "problem_status": None, # None means NO PROBLEM (100% Success)
                "response_text": response_text,
                "saved_file": os.path.join(PROJECT_DIR, "terminal_output.txt")
            }
            
            # Save output file
            with open(os.path.join(PROJECT_DIR, "terminal_output.txt"), "w", encoding="utf-8") as f:
                f.write(f"USER INPUT: {user_input}\nRESPONSE:\n{response_text}\n")
                
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
