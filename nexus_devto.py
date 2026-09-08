import json
import requests
import webbrowser
import urllib.parse

class DuckDuckGoDevToAI:
    """محرك مخصص لتوليد مقالات برمجية احترافية لجلب الشركات والمستثمرين عبر Dev.to"""
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

    def generate_article(self, prompt):
        vqd = self._get_token()
        if not vqd: return "Error connecting to AI."
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
            return full_res
        except Exception as e: return f"Error: {e}"


class DevToAutonomousMarketer:
    def __init__(self):
        self.repo_url = "https://github.com"
        self.genesis_wallet = "0xa3dCED521c887C5b46e77F807330097245d80E35"
        self.ai = DuckDuckGoDevToAI()
        print("="*60)
        print("🚀 تم تشغيل محرك [DevToAutonomousMarketer] الخالي من الـ API Key!")
        print("="*60)

    def launch_viral_article(self):
        """توليد مقالة برمجية خارقة وفتح متصفحك تلقائياً لنشرها دون حظر"""
        print("\n[🧠 معالجة] جاري صياغة مقالة علمية مبهرة لجذب كبار المستثمرين ومطوري الويب 3...")
        
        prompt = f"""
        Write a viral, highly professional technical article for Dev.to platform.
        Title: How a Self-Evolving AI Protocol on Polygon is Disrupting the Tech Economy.
        The article must explain the future of autonomous agent code that earns micro-transactions directly to a user's wallet.
        Include sections: Introduction, Core Architecture, The Economics, and How to Test It.
        Politely invite developers and investors to view the open-source repository here: {self.repo_url}
        Mention the genesis protocol payment wallet for verification: {self.genesis_wallet}
        Format the output in clean Markdown.
        """
        
        article_markdown = self.ai.generate_article(prompt)
        
        print("\n[✅ نجاح التوليد] تم تجهيز المقالة التسويقية بنجاح!")
        print("🌍 جاري فتح صفحة النشر المباشرة على Dev.to في متصفحك الآن...")
        
        # الرابط المباشر لكتابة المقالات في Dev.to
        devto_editor_url = "https://dev.to"
        
        # فتح المتصفح التلقائي للجهاز أمامك مباشرة
        webbrowser.open(devto_editor_url)
        
        # طباعة المقالة في ملف نصي محلي لتنسخها وتلصقها بثانية واحدة
        with open("devto_article.txt", "w", encoding="utf-8") as f:
            f.write(article_markdown)
            
        print("\n" + "="*50)
        print("📋 [إرشادات خطوة واحدة]:")
        print("1. تم فتح موقع Dev.to الآن في متصفحك.")
        print("2. افتح الملف النصي الجديد الذي تم إنشاؤه بجانب الكود باسم: (devto_article.txt)")
        print("3. انسخ محتواه، والصفه في الموقع واضغط Publish!")
        print("🔥 بهذه الطريقة حصلت على دعاية عالمية حية أمام ملايين الشركات وبصفر تكلفة وبدون الـ API Key المعقد.")
        print("="*50)

if __name__ == "__main__":
    marketer = DevToAutonomousMarketer()
    marketer.launch_viral_article()
