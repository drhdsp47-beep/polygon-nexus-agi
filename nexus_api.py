import json
import requests
from http.server import BaseHTTPRequestHandler, HTTPServer
from web3 import Web3

class DuckDuckGoBackendAI:
    def __init__(self):
        self.status_url = "https://duckduckgo.com"
        self.chat_url = "https://duckduckgo.com"
        self.model = "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo"
    
    def _get_token(self):
        headers = {"x-vqd-accept": "1", "User-Agent": "Mozilla/5.0"}
        try:
            res = requests.get(self.status_url, headers=headers)
            return res.headers.get("x-vqd-4")
        except: return None

    def ask(self, prompt):
        vqd = self._get_token()
        if not vqd: return "خطأ في الاتصال بعقل النظام السحابي."
        headers = {"x-vqd-4": vqd, "Content-Type": "application/json", "Accept": "text/event-stream", "User-Agent": "Mozilla/5.0"}
        payload = {"model": self.model, "messages": [{"role": "user", "content": prompt}]}
        try:
            res = requests.post(self.chat_url, headers=headers, json=payload)
            lines = res.text.split("\n")
            full_res = ""
            for line in lines:
                if line.startswith("data:"):
                    chunk = line[5:].strip()
                    if chunk == "[DONE]": break
                    try:
                        chunk_json = json.loads(chunk)
                        if "message" in chunk_json: full_res += chunk_json["message"]
                    except: continue
            return full_res if full_res else "تمت معالجة الطلب عبر بايثون بنجاح."
        except Exception as e: return f"خطأ في النواة: {e}"

# إعداد خادم بايثون لاستقبال طلبات الويب
class SimpleAPIHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        # السماح لموقع GitHub Pages بالاتصال بكود بايثون دون حظر (CORS)
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_POST(self):
        self.do_OPTIONS()
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))
        
        user_prompt = data.get("prompt", "")
        
        # استدعاء عقل بايثون المربوط بـ DuckDuckGo
        ai_backend = DuckDuckGoBackendAI()
        ai_response = ai_backend.ask(user_prompt)
        
        # إرسال النتيجة إلى واجهة GitHub Pages
        response_data = {
            "status": "success",
            "reply": ai_response,
            "wallet": "0xa3dCED521c887C5b46e77F807330097245d80E35"
        }
        
        self.wfile.write(json.dumps(response_data).encode('utf-8'))

def run_server():
    # تشغيل الخادم على المنفذ 8000
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, SimpleAPIHandler)
    print("🚀 خادم بايثون الخلفي نشط ومستعد لاستقبال طلبات GitHub Pages على المنفذ 8000...")
    httpd.serve_forever()

if __name__ == "__main__":
    run_server()
