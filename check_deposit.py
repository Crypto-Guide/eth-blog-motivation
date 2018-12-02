from lib.transactions import check_deposit
from ethblogapp.models import User

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.models import (
    TextSendMessage,
)


# 現在、finish_deposit_checkがFalseのuserを定期的に(毎分)デポジット入金があったかチェックする

# LINE botのSECRETs
YOUR_CHANNEL_SECRET = '907c0586c0380686029281c38f6d25c8'
YOUR_CHANNEL_ACCESS_TOKEN = 'Dt4pGNCFjNQ6Ve/8HeLx0lXhpdoFP7DzNLeTTsXGjRzcz572EwZhYiSvLKbDh5+C+PaDeFvZ/LPQKvqUTwzVmOX7s6i9Tr6skVIsinGeZfd1BAK5bVICw5Btv3n0DW4HUqWIYS7xlwrNhUYJl9oB9gdB04t89/1O/w1cDnyilFU='

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)


records = User.query.all()

for record in records:
    result = check_deposit(record.address)
    if result == True:
        line_bot_api.push_message(record.line_id, TextSendMessage(text='デポジットが確認できました。今日からブログの毎日更新、頑張って下さい。'))

