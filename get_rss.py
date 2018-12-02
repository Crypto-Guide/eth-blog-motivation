from ethblogapp.models import User
import datetime
from ethblogapp.database import db_session
from lib.scraping import get_article_titles_from_blog_url
from lib.transactions import return_user_deposit
from lib.transactions import remove_user_deposit

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.models import (
    TextSendMessage,
)

# 1日に一回定期実行される「ブログが更新されているかを確認する」スクリプト

YOUR_CHANNEL_SECRET = 'fa1ae7996425f562e20ac287f05907b4'
YOUR_CHANNEL_ACCESS_TOKEN = 'gxD4uLAcxFgWZWwCc3LRRbJF/M85aIZ1pY3MBnpj3ZO+HuHQQmQx8lEJs3TXL+NC+PaDeFvZ/LPQKvqUTwzVmOX7s6i9Tr6skVIsinGeZfcIgumAfT8K2pKLD9X70OzIvk7IjyPfnnI2Ko03JF92uQdB04t89/1O/w1cDnyilFU='

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)


columns = User.query.all()

for column in columns:
    target_date_in_db = column.target_date
    target_date = target_date_in_db.date()

    now = datetime.datetime.now()
    today = datetime.date.today()

    if target_date is None:
        continue

    if target_date < today:
        continue

    to = column.line_id
    url = column.url
    address = column.address

    title_array = get_article_titles_from_blog_url(url)
    last_article_title = title_array[0]

    if last_article_title == column.last_article_title:
        # JSのEther没収TX APIを叩く
        remove_user_deposit(address)
        line_bot_api.push_message(to, TextSendMessage(text='ブログの更新をサボりましたね。Etherが没収されました。'))
    else:
        if today == target_date:
            # JSのロック解除TX APIを叩く
            return_user_deposit(address)
            line_bot_api.push_message(to, TextSendMessage(text='継続目標を達成しました！DepositしていたEtherに継続へのご褒美分をプラスして貴方のアドレスに送金されました！'))

        column.last_article_title = last_article_title
        column.updated_at = now
        db_session.add(column)
        db_session.commit()
        line_bot_api.push_message(to, TextSendMessage(text='今日もブログを更新したんですね！素晴らしい！この調子で継続しましょう'))