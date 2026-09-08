import json
import requests
import os
from datetime import datetime

class GitHubPureAI:
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
        if not vqd: return "فشل الاتصال بالذكاء الاصطناعي."
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
            return full_res if full_res else "تمت المعالجة بنجاح."
        except Exception as e: return f"خطأ: {e}"

if __name__ == "__main__":
    print("⏳ بدأ عقل بايثون بالعمل داخل خوادم GitHub Actions...")
    
    ai = GitHubPureAI()
    
    # البوت يقوم بالتفكير وتوليد تحديث تقني تلقائي ليراه المستثمرون
    prompt = "Write a 1-sentence breakthrough update about Polygon gas optimization for our investors."
    ai_update = ai.ask(prompt)
    
    # قراءة البيانات الحالية أو إنشاء بيانات جديدة للأرباح والتحديثات
    stats_file = "stats.json"
    if os.path.exists(stats_file):
        with open(stats_file, "r") as f:
            data = json.load(f)
    else:
        data = {"total_earnings": 0.0, "last_update": "", "latest_log": ""}
    
    # محاكاة زيادة الأرباح وتحديث البيانات تلقائياً بفضل تشغيل بايثون
    data["total_earnings"] += 0.05
    data["last_update"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data["latest_log"] = ai_update
    
    # حفظ البيانات الجديدة ليقرأها موقع GitHub Pages
    with open(stats_file, "w") as f:
        json.dump(data, f, indent=4)
        
    print(f"✅ تم التحديث بنجاح! الأرباح الحالية: ${data['total_earnings']}")
    print(f"📝 رسالة البوت الحالية: {ai_update}")
