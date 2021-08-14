# -*- coding: UTF-8 -*-
import os
from datetime import datetime
from flask import Flask, abort, request
from datetime import datetime
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

line_bot_api = LineBotApi(os.environ.get("CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.environ.get("CHANNEL_SECRET"))

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    
    try:
        print(body, signature)
        handler.handle(body, signature)
        
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def pretty_echo(event):

    sum = 0

    for i in event.message.text.splitlines():
        a = i.split(" ")
        d1 = datetime.strptime(a[0], '%H:%M')
        d2 = datetime.strptime(a[1], '%H:%M')
        minutes_diff = (d2 - d1).total_seconds() / 60.0
        minutes_diff = minutes_diff - (minutes_diff % 5)
        sum += minutes_diff
    
    hour = int(sum // 60)
    minute = int(sum % 60)
        
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="總共" + str(hour) + "小時" + str(minute) + "分鐘")
    )

if __name__ == "__main__":
    app.run()