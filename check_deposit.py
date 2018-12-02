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
YOUR_CHANNEL_SECRET = 'fa1ae7996425f562e20ac287f05907b4'
YOUR_CHANNEL_ACCESS_TOKEN = 'gxD4uLAcxFgWZWwCc3LRRbJF/M85aIZ1pY3MBnpj3ZO+HuHQQmQx8lEJs3TXL+NC+PaDeFvZ/LPQKvqUTwzVmOX7s6i9Tr6skVIsinGeZfcIgumAfT8K2pKLD9X70OzIvk7IjyPfnnI2Ko03JF92uQdB04t89/1O/w1cDnyilFU='

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)


records = User.query.all()

for record in records:
    result = check_deposit(record.address)
    if result == True:
        line_bot_api.push_message(record.line_id, TextSendMessage(text='デポジットが確認できました。今日からブログの毎日更新、頑張って下さい。'))

