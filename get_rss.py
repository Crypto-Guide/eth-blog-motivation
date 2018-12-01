from ethblogapp.models import User
import urllib.request
import urllib.error
from bs4 import BeautifulSoup
import feedparser
import re
from datetime import datetime
from ethblogapp.database import db_session

# def check_blogs():

columns = User.query.all()

for column in columns:
    target_date = column.target_date
    if target_date > datetime.now:
        continue

    url = column.url

    if not re.match(r"^https?:\/\/", url):
        print("value(%s) is not URL" % url)
        continue

    html = urllib.request.urlopen(url)
    soup = BeautifulSoup(html, 'lxml')
    link_tags = soup.find_all("link")
    paths = map(lambda path: path.get('href'), link_tags)

    for path in paths:
        if '/rss' in path:
            feed_url = path
            continue

        if '/feed' in path and '/comments' not in path:
            feed_url = path

    # RSSから記事タイトルを取得
    feed_result = feedparser.parse(feed_url)

    if feed_result is None:
        continue

    # 記事タイトルを取得し表示
    for entry in feed_result.entries:
        print(entry.title)

    last_article_title = feed_result.entries[0].title
    print(last_article_title)

    if last_article_title == column.last_article_title:
        print("Remove ETH !")
    else:
        column.last_article_title = last_article_title
        column.updated_at = datetime.now()
        db_session.add(column)
        db_session.commit()
        print("update Blog Article! Great!")