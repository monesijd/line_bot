# 環境建置

## 建立 line 機器人

### 創建 line 的官方帳號並進入控制台

由此創建帳號或登入 https://developers.line.biz 

### create 一個新的 Provider，並創建一個新的channel

填入 Provider 的名稱，並按下create

選擇 Messaging API，並設定 channel 的名稱(機器人的分類可以自己選)

### 設定機器人

進入 basic settings，記下 Channel secret

進入 Messaging API
- 將 webhook 打開
- 產生 Channel access token，並記下等等用
- 記下 Bot basic ID
  
## 開啟回應聊天功能

進入 https://manager.line.biz ，找到機器人，並往下滑找到"回應設定"按鈕，將聊天和 Webhook 打開，確保機器人正常回復
