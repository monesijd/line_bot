import os
import urllib.request
from flask import Flask, request, abort


from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
)

app = Flask(__name__)

# 從環境變數讀取 token
configuration = Configuration(access_token=os.environ['LINE_ACCESS_TOKEN'])
handler = WebhookHandler(os.environ['LINE_SECRET'])


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        if event.message.text == "登革熱":
            bot = urllib.request.urlopen("https://khweb.geohealth.tw/")
            web_content = bot.read().decode('utf8')
            for each_find in re.findall(r"<h5.+?>(/w+?)<span.+?>(/w/w)", web_content):
                print(f'{each_find[0]}: {each_find[1]}')
        else:
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text=event.message.text)]
                )
            )

if __name__ == "__main__":
    app.run()