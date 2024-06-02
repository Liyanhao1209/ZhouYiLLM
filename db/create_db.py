from dataclasses import dataclass
import datetime
from typing import List

from sqlalchemy import ForeignKey, create_engine, Column, Text, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column, relationship

Base = declarative_base()


# 用户表
class User(Base):
    __tablename__ = 'User'

    id: Mapped[str] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column()  # 一个邮箱只能注册一个账号
    password: Mapped[str] = mapped_column()
    name: Mapped[str] = mapped_column()
    is_active: Mapped[bool] = mapped_column(default=True)  # 是否被封禁
    age: Mapped[int] = mapped_column()
    sex: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()

    conversations: Mapped[List["Conversation"]] = relationship(back_populates='owner')  # 拥有的会话集合
    blogs: Mapped[List["Blog"]] = relationship(back_populates='owner')  # 拥有的博客集合
    comments: Mapped[List["Comment"]] = relationship(back_populates='owner')  # 拥有的评论集合
    knowledge_bases: Mapped[List["KnowledgeBase"]] = relationship(back_populates='owner')  # 拥有的知识库集合

    def __repr__(self):
        return f'<User(id={self.id}, email={self.email}, name={self.name})>'


# 会话表
class Conversation(Base):
    __tablename__ = 'Conversation'

    id: Mapped[str] = mapped_column(primary_key=True)
    conv_name: Mapped[str] = mapped_column()
    create_time: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.utcnow())
    user_id: Mapped[str] = mapped_column(ForeignKey('User.id'))

    owner: Mapped["User"] = relationship(back_populates='conversations')
    records: Mapped[List["Record"]] = relationship(back_populates='conversation')

    def __repr__(self):
        return f'<Conversation(id={self.id}, conv_name={self.conv_name})>'


# 博客表
class Blog(Base):
    __tablename__ = "Blog"

    id: Mapped[str] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column()
    content: Mapped[Text] = Column(Text)
    create_time: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.utcnow())
    user_id: Mapped[str] = mapped_column(ForeignKey('User.id'))

    owner: Mapped["User"] = relationship(back_populates='blogs')
    comments: Mapped[List["Comment"]] = relationship(back_populates='blog')

    def __repr__(self):
        return f'<Blog(id={self.id}, title={self.title})>'


# 评论表
class Comment(Base):
    __tablename__ = "Comment"

    id: Mapped[str] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column()
    create_time: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.utcnow())
    user_id: Mapped[str] = mapped_column(ForeignKey('User.id'))
    blog_id: Mapped[str] = mapped_column(ForeignKey('Blog.id'))

    owner: Mapped["User"] = relationship(back_populates='comments')
    blog: Mapped["Blog"] = relationship(back_populates='comments')

    def __repr__(self):
        return f'<Comment(id={self.id}, content={self.content})>'


# 知识库表
class KnowledgeBase(Base):
    __tablename__ = "KnowledgeBase"

    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    create_time: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.utcnow())
    user_id: Mapped[str] = mapped_column(ForeignKey('User.id'))

    owner: Mapped["User"] = relationship(back_populates='knowledge_bases')

    def __repr__(self):
        return f'<KnowledgeBase(id={self.id}, name={self.name})>'


# 管理员表
class Administrator(Base):
    __tablename__ = "Administrator"

    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    password: Mapped[str] = mapped_column()

    def __repr__(self):
        return f'<Administrator(id={self.id}, name={self.name})>'


# 聊天记录表
class Record(Base):
    __tablename__ = "Record"

    id = Column(Integer, primary_key=True, autoincrement=True)
    content: Mapped[str] = mapped_column()
    is_ai: Mapped[bool] = mapped_column()
    conv_id: Mapped[str] = mapped_column(ForeignKey('Conversation.id'))

    conversation: Mapped["Conversation"] = relationship(back_populates='records')

    def __repr__(self):
        return f'<Record(id={self.id}, content={self.content})>'


if __name__ == '__main__':
    engine = create_engine("sqlite:///zhouyi_web.db", echo=True)
    Base.metadata.create_all(engine)
