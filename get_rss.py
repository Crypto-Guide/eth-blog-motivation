from ethblogapp.models import User
from datetime import datetime
from ethblogapp.database import db_session
from lib.scraping import get_article_titles_from_blog_url



columns = User.query.all()

for column in columns:
    target_date = column.target_date
    if target_date is None:
        continue

    if target_date > datetime.now:
        continue

    url = column.url

    title_array = get_article_titles_from_blog_url(url)
    last_article_title = title_array[0]

    if last_article_title == column.last_article_title:
        print("Remove ETH !")
    else:
        column.last_article_title = last_article_title
        column.updated_at = datetime.now()
        db_session.add(column)
        db_session.commit()
        print("update Blog Article! Great!")