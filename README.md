# 環境建置

## 建立 line 機器人

### 創建 line 的官方帳號並進入控制台

由此創建帳號或登入 https://developers.line.biz 

### 新增一個新的 Provider，創建一個channel

建立一個 Provider 填入名稱，進去後建立 Messaging API channel(機器人的分類可以自己選)

建立完成請記下以下資訊:

進入 basic settings
- Channel secret

進入 Messaging API
- 產生 Channel access token 並記下
- Bot basic ID
  
### 開啟回應聊天功能

進入 https://manager.line.biz ，找到機器人，並往下滑找到"回應設定"按鈕，將聊天和 Webhook 打開，確保機器人正常回復

## 在 render 網站上開設帳號

登入 github 後，進入 https://render.com/ 用 github 帳號登入

## 在 github 上建立一個 line 機器人的 repository

建立一個 repo，下列將用範例繼續說明: https://github.com/monesijd/line_bot

## 到 linux 機器上將 line 機器人 clone 下來

```bash
python3 clone https://github.com/monesijd/line_bot
```

## 建立 venv 環境，安裝套件

```bash
cd git/line_bot/
python3 -m venv .venv 
source .venv/bin/activate
pip install pip setuptools wheel -U
pip install flask line-bot-sdk gunicorn
pip freeze > requirements.txt
```

## 測試 line-bot-sdk 所提供的程式碼

Python 版的 line-bot-sdk github 網址在 https://github.com/line/line-bot-sdk-python

以下是官方的範例作微調，並存成 app.py

```python
import os
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
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=event.message.text)]
            )
        )

if __name__ == "__main__":
    app.run()
```

## 建立 render 專案

點擊右上角 new+ -> Web Service -> Build and deploy from a Git repository

1. Region 選擇 Singapore
2. Start Command 輸入 gunicorn app:app
3. 將前面拿到的 line access token 和 secret 填入 Environment Variables： a. LINE_SECRET b. LINE_ACCESS_TOKEN

按下 Create Web Service 完成建置

## 將完成建置的 render 網址填入 line webhook

回到 line 的 Messaging API 頁面，將新建立的 https://xxxxxxxxxx.onrender.com/callback 填入 Webhook URL ，並且把下方的 Use webhook 設定為啟用

## 讓 render 的服務不會進入休眠

找一台 linux 機器， 進去後執行

```bash
crontab -e
```

輸入以下排程，每分鐘去戳 render 的專案，讓它不要睡著

```
* * * * * curl https://xxxxxxxxxx.onrender.com/callback
```
