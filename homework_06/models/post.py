from sqlalchemy import Column, Integer, String

from .database import db


class Post(db.Model):
    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String(30))
    title = Column(String(100))
    body = Column(String(300))

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.title!r}>"
