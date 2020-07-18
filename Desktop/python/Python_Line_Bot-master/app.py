#!/usr/bin/env python3  
# -*- coding: utf-8 -*-  
"""  
@desc:  
@author: TsungHan Yu  
@contact: nick.yu@hzn.com.tw  
@software: PyCharm  @since:python 3.6.0 on 2017/7/13
"""

import os
import requests
import configparser

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

# LINE 聊天機器人的基本資料
config = configparser.ConfigParser()
config.read('config.ini')

line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))
handler = WebhookHandler(config.get('line-bot', 'channel_secret'))

# ACCESS_TOKEN = os.environ.get('0+asibQsKgoDXCkGyj/cIY4PizB9wnDXFqaFfwLePpfX2HInip9zr2U1OVhQCty/wHHI1PlfSeJmhixau0xTdC/uUaGz2N5kFX1UKmrjFRsM0fuoiE/mjS7eW0xl2LIlT39ikCbkfgHbHpH8AvZoaAdB04t89/1O/w1cDnyilFU=')
# SECRET = os.environ.get('61ac96f990110b7b7c9e9ca081b039d9')

# line_bot_api = LineBotApi(ACCESS_TOKEN)
# handler = WebhookHandler(SECRET)


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
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    res = event.message.text
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=res))


if __name__ == "__main__":
    app.run()
