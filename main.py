import requests

# تنظیمات آدرس API Flowise
FLOWISE_API_URL = "http://flow.gpantex.com/api/v1/prediction/<flow-id>"  # آیدی فلو را جایگزین کن
# اگر Flowise نیاز به کلید API دارد، این خط را فعال کن و مقداردهی کن
# FLOWISE_API_KEY = "<YOUR_API_KEY>"

def on_message_received(message, user_id=None, context=None):
    """
    این تابع پیام‌های دریافتی را چک می‌کند و اگر با دستور /flowise شروع شده باشد،
    پرسش را به Flowise می‌فرستد و پاسخ را برمی‌گرداند.
    """
    if message.startswith("/flowise "):   # فقط پیام‌هایی که با این دستور شروع شود
        user_prompt = message[len("/flowise "):].strip()
        payload = {"input": user_prompt}
        headers = {"Content-Type": "application/json"}
        # اگر کلید API نیاز است، این خط را فعال کن:
        # headers["Authorization"] = f"Bearer {FLOWISE_API_KEY}"
        try:
            resp = requests.post(FLOWISE_API_URL, json=payload, headers=headers, timeout=15)
            resp.raise_for_status()
            res_data = resp.json()
            # پاسخ را از خروجی مناسب استخراج می‌کنیم
            reply = res_data.get("text") or res_data.get("output") or str(res_data)
            return reply
        except Exception as e:
            return f"❌ خطا در ارتباط با Flowise: {e}"
    # در غیر این صورت، هیچ پاسخی برگشت داده نشود
    return None

def register_plugin(plugin_manager):
    plugin_manager.register_message_handler(on_message_received)
