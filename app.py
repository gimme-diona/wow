from flask import Flask, request, abort
from linebot import ( LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (MessageEvent, TextMessage, TextSendMessage ,)

app = Flask(__name__)

line_bot_api= LineBotApi('Channel access token')
handler = WebhookHandler('Channel secret')

@app.route("/", methods=['GET'])
def index():
    name = request.args.get('name')
    if name==None: #<--有沒傳入任何url的參數
        name="" #<--防止 "Hello"+name 出現 TypeError: can only concatenate str (not "NoneType") to str
    return "Hello"+name

@app.route("/linebot", methods=['POST'])
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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage) #當有收到訊息事件且訊息是文字格式則執行handle_message(),MsgTpe參考https://ithelp.ithome.com.tw/articles/10217402
def handle_message(event):#function name可以自定
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))

if __name__ == "__main__":
    app.run()
