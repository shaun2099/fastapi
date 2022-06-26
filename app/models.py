from .database import Base
from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.sql import expression
from sqlalchemy.orm import declarative_base, relationship


class Post(Base):
    __tablename__ = "post"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, nullable=False, server_default=expression.true())
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=expression.text('CURRENT_TIMESTAMP'))
    owner_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"),  nullable=False)

    # "User" is py class User
    owner = relationship("User")

    # def __init__(self, title, content, published=True):
    #     self.title = title
    #     self.content = content
    #     self.published = published


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, nullable=False)
    # username = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    # full_name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=expression.text('CURRENT_TIMESTAMP'))

    # def __init__(self, username, email, full_name, password):
    #     self.username = username
    #     self.email = email
    #     self.full_name = full_name
    #     self.password = password