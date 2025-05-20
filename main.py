from langbot_plugin_base import PluginBase
import requests

class FlowisePlugin(PluginBase):
    # متادیتا پلاگین - این موارد باید حتماً باشند
    name = "FlowisePlugin"
    description = "Connect Langbot to FlowiseAI"
    author = "vahid162"
    version = "1.0.0"
    
    # تعریف دستورات
    def commands(self):
        return [
            {
                "name": "flowise",
                "description": "سوال خود را به Flowise ارسال و پاسخ هوشمند دریافت کنید",
                "usage": "/flowise <متن سوال شما>"
            }
        ]
    
    # ثبت handler اصلی پیام‌ها
    def on_message(self, message, context):
        if message.content.strip().startswith("/flowise"):
            question = message.content.replace("/flowise", "", 1).strip()
            if not question:
                return "لطفا سوال خود را پس از /flowise بنویسید"
            
            # آدرس فلو را اینجا قرار بده
            FLOWISE_API_URL = "https://flow.gpantex.com/api/v1/prediction/50defcc1-aed6-40ba-9dd5-4330e1d2313b"
            
            payload = {"input": question}
            headers = {"Content-Type": "application/json"}
            # اگر Flowise کلید می‌خواهد:
            # headers["Authorization"] = "Bearer <API_KEY>"
            
            try:
                r = requests.post(FLOWISE_API_URL, json=payload, headers=headers, timeout=15)
                r.raise_for_status()
                res_data = r.json()
                reply = res_data.get("text") or res_data.get("output") or str(res_data)
                return reply
            except Exception as e:
                return f"❌ خطا در ارتباط با Flowise: {e}"

        return None  # اگر دستور نبود هیچ اتفاقی نمی‌افتد

def setup():
    return FlowisePlugin()
