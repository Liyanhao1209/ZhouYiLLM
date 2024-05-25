from datetime import datetime

from sqlalchemy import ForeignKey, create_engine, Column, Text
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

    conversations = relationship('Conversation', back_populates='owner')  # 拥有的会话集合
    blogs = relationship('Blog', back_populates='owner')  # 拥有的博客集合
    comments = relationship('Comment', back_populates='owner')  # 拥有的评论集合
    knowledge_bases = relationship('KnowledgeBase', back_populates='owner')  # 拥有的知识库集合

    def __repr__(self):
        return f'<User(id={self.id}, email={self.email}, name={self.name})>'


# 会话表
class Conversation(Base):
    __tablename__ = 'Conversation'

    id: Mapped[str] = mapped_column(primary_key=True)
    conv_name: Mapped[str] = mapped_column()
    create_time: Mapped[datetime] = mapped_column()
    user_id: Mapped[str] = mapped_column(ForeignKey('User.id'))

    owner = relationship('User', back_populates='conversations')

    def __repr__(self):
        return f'<Conversation(id={self.id}, conv_name={self.conv_name})>'


# 博客表
class Blog(Base):
    __tablename__ = "Blog"

    id: Mapped[str] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column()
    content: Mapped[Text] = Column(Text)
    create_time: Mapped[datetime] = mapped_column()
    user_id: Mapped[str] = mapped_column(ForeignKey('User.id'))

    owner = relationship('User', back_populates='blogs')
    comments = relationship('Comment', back_populates='blog')

    def __repr__(self):
        return f'<Blog(id={self.id}, title={self.title})>'


# 评论表
class Comment(Base):
    __tablename__ = "Comment"

    id: Mapped[str] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column()
    create_time: Mapped[datetime] = mapped_column()
    user_id: Mapped[str] = mapped_column(ForeignKey('User.id'))
    blog_id: Mapped[str] = mapped_column(ForeignKey('Blog.id'))

    owner = relationship('User', back_populates='comments')
    blog = relationship('Blog', back_populates='comments')

    def __repr__(self):
        return f'<Comment(id={self.id}, content={self.content})>'


# 知识库表
class KnowledgeBase(Base):
    __tablename__ = "KnowledgeBase"

    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    create_time: Mapped[datetime] = mapped_column()
    user_id: Mapped[str] = mapped_column(ForeignKey('User.id'))

    owner = relationship('User', back_populates='knowledge_bases')

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


if __name__ == '__main__':
    engine = create_engine("sqlite:///zhouyi_web.db", echo=True)
    Base.metadata.create_all(engine)
