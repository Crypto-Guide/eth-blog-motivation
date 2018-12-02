from flask import Flask, abort, request
from ethblogapp.models import User
import datetime
import re
from lib.scraping import get_blog_title_from_url
from lib.transactions import get_new_user_address
from ethblogapp.database import db_session

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
app.config['DEBUG'] = True

# LINE botのSECRETs
YOUR_CHANNEL_SECRET = '907c0586c0380686029281c38f6d25c8'
YOUR_CHANNEL_ACCESS_TOKEN = 'Dt4pGNCFjNQ6Ve/8HeLx0lXhpdoFP7DzNLeTTsXGjRzcz572EwZhYiSvLKbDh5+C+PaDeFvZ/LPQKvqUTwzVmOX7s6i9Tr6skVIsinGeZfd1BAK5bVICw5Btv3n0DW4HUqWIYS7xlwrNhUYJl9oB9gdB04t89/1O/w1cDnyilFU='

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

# line bot用関数
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

# line botメッセージ返信用関数
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_user_id = event.source.user_id

    if re.match(r"^https?:\/\/", event.message.text):
        url = event.message.text

        content = User.query.filter_by(line_id=line_user_id).first()
        if content is None:
            content = User(line_id=line_user_id, address=None, url=url)
        else:
            content.url = url
        db_session.add(content)
        db_session.commit()

        blog_title = get_blog_title_from_url(url)
        address_private_key_json = get_new_user_address(line_user_id)
        user_address = address_private_key_json['address']
        private_key = address_private_key_json['privateKey']

        reply_array = [TextSendMessage(text="貴方のBlog「" + blog_title + "」が毎日更新されているか、監視するプログラムが作動しました。"), TextSendMessage(text="以下のDeposit用addressをコピーし、walletからEtherをデポジットして下さい"), TextSendMessage(text="アドレス：" + user_address), TextSendMessage(text= "秘密鍵：" + private_key)]
        line_bot_api.reply_message(
            event.reply_token,
            reply_array
            )
    elif "日" in event.message.text and "継続" in event.message.text:
        continue_day_str = event.message.text.split("日")
        continue_day_num = continue_day_str[0]
        if continue_day_num is None:
            abort(404)

        now = datetime.datetime.now()
        target_date = now + datetime.timedelta(days=int(continue_day_num))

        content = User.query.filter_by(line_id=line_user_id).first()
        if content is None:
            content = User(line_id=line_user_id, address=None, url=None, target_date=target_date)
        else:
            return
        db_session.add(content)
        db_session.commit()

        date_str = target_date.strftime('%Y/%m/%d')

        reply_array = [TextSendMessage(text="今日から" + date_str + "まで、" + continue_day_num + "日間、毎日更新を継続するのですね。"), TextSendMessage(text="貴方のBlogのURLを送信して下さい。")]
        line_bot_api.reply_message(
            event.reply_token,
            reply_array
        )
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='関係ないことをLINEしてる暇があるんですか？そんなんだからブログが続かないんですよ。'))



@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()



if __name__ == "__main__":
    app.run()