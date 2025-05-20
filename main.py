from langplugin.plugin import Plugin, on_message
import requests

class FlowisePlugin(Plugin):
    def __init__(self):
        super().__init__(
            name="FlowisePlugin",
            version="1.0.0",
            author="vahid162",
            description="Flowise API connector for Langbot"
        )

    @on_message
    def handle_message(self, ctx):
        if ctx.content.strip().startswith('/flowise'):
            user_question = ctx.content[len('/flowise'):].strip()
            if not user_question:
                return "لطفاً سوال خود را بعد از /flowise بنویسید."

            FLOWISE_API_URL = "https://flow.gpantex.com/api/v1/prediction/50defcc1-aed6-40ba-9dd5-4330e1d2313b"
            payload = {"input": user_question}
            headers = {"Content-Type": "application/json"}
            # اگر کلید API لازم بود اضافه کن:
            # headers["Authorization"] = "Bearer <API_KEY>"
            try:
                r = requests.post(FLOWISE_API_URL, json=payload, headers=headers, timeout=15)
                r.raise_for_status()
                res = r.json()
                reply = res.get("text") or res.get("output") or str(res)
                return reply
            except Exception as e:
                return f"❌ خطا در ارتباط با Flowise: {e}"

def setup():
    return FlowisePlugin()
