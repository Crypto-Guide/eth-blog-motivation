from sqlalchemy import Column, Integer, String, Text, DateTime
from ethblogapp.database import Base
from datetime import datetime


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    address = Column(String(128), unique=True)
    url = Column(String(128), unique=True)
    target_date = Column(DateTime)
    last_article_title = Column(Text)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())

    def __init__(self, address=None, url=None, target_date=None, last_article_title=None):
        self.address = address
        self.url = url
        self.target_date = target_date
        self.last_article_title = last_article_title

    def __repr__(self):
        return '<Address %r>' % (self.address)