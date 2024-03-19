import os
import sys
import enum
from sqlalchemy import Enum
from sqlalchemy import Column, ForeignKey, Integer, Table, String
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()

class MyEnum(enum.Enum):
    video = 1
    picture = 2
    
follower_user = Table('follower_user', Base.metadata,
    Column('follower_id', Integer, ForeignKey('follower.id')),
    Column('user_id', Integer, ForeignKey('user.id')))

class Follower(Base):
    __tablename__ = 'follower'
    id = Column(Integer, primary_key=True)
    follower_name = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship("User", secondary=follower_user, back_populates="follower")

class Media(Base):
    __tablename__ = 'media'
    id = Column(Integer, primary_key=True)
    url = Column(String(250), nullable=False)
    type = Column(Enum(MyEnum), nullable=False)
    post_id = Column(Integer, ForeignKey('post.id'))

class Comment(Base):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True)
    comment_text = Column(String(500), nullable=False)
    post_id = Column(Integer, ForeignKey('post.id'))
    user_id = Column(Integer, ForeignKey('user.id'))

class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    media = relationship(Media)
    comment = relationship(Comment)

class user(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    follower = relationship("Follower", secondary=follower_user, back_populates="user")
    post = relationship(Post)
    comment = relationship(Comment)

  

## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e

#   def to_dict(self):
#         return {}