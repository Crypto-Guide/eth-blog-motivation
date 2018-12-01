import urllib.request
import urllib.error
from bs4 import BeautifulSoup
import feedparser
import re

def get_article_titles_from_blog_url(url):
    if not re.match(r"^https?:\/\/", url):
        print("value(%s) is not URL" % url)
        raise Exception('Argument is not URL')

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
        raise Exception("This page has no rss feed or articles.")

    title_array = []

    # 記事タイトルを取得し配列に格納
    for entry in feed_result.entries:
        print(entry.title)
        title_array.append(entry.title)

    return title_array


def get_blog_title_from_url(url):
    if not re.match(r"^https?:\/\/", url):
        print("value(%s) is not URL" % url)
        raise Exception('Argument is not URL')

    html = urllib.request.urlopen(url)
    soup = BeautifulSoup(html, 'lxml')
    site_title = soup.find("title")

    return site_title.string