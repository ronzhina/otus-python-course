import os

from sqlalchemy import Column, Integer, String
from sqlalchemy import ForeignKey
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, relationship, declared_attr
from sqlalchemy.orm import sessionmaker


class Base:
    @declared_attr
    def __tablename__(self):
        return f"{self.__name__.lower()}s"

    id = Column(Integer, primary_key=True, nullable=False)


PG_CONN_URI = os.environ.get("SQLALCHEMY_PG_CONN_URI") or "postgresql+asyncpg://user:password@localhost:5432/postgres"
engine = create_async_engine(PG_CONN_URI, echo=True)
Base = declarative_base(bind=engine, cls=Base)
Session = sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession,
)


class User(Base):
    name = Column(String(32))
    username = Column(String(32))
    email = Column(String(32))

    posts = relationship("Post", back_populates="user")

    def __repr__(self):
        return str(self)

    def __init__(self, name, username, email):
        self.name = name
        self.username = username
        self.email = email


class Post(Base):
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String(100))
    body = Column(String(300))

    user = relationship("User", back_populates="posts")

    def __repr__(self):
        return str(self)

    def __init__(self, user_id, title, body):
        self.user_id = user_id
        self.title = title
        self.body = body
