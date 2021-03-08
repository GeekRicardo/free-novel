#!/User/ricardo/anaconda3/bin/python
# -*- encoding: utf-8 -*-
'''
@File     :  models.py
@Time     :  2020/10/23 16:58:40
@Author   :  Ricardo
@Version  :  1.0
@Desc     :  实体类
'''

# import lib here
from . import db

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    passwd = db.Column(db.String(50))
    level = db.Column(db.Integer)

    def __str__(self):
        return self.username

    def __init__(self, **kwargs):
        super().__init__()
        if(not len(kwargs) == 0):
            self.id = kwargs.get('id')
            self.username = kwargs.get('username')
            self.passwd = kwargs.get('passwd')
            self.level = kwargs.get('level')


class TXT(db.Model):
    __tablename__ = "txt"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    author = db.Column(db.String(50))
    url = db.Column(db.String(100))

    def __init__(self, txtname, author, room) -> None:
        self.title = txtname
        self.url = room
        self.author = author

    def __str__(self):
        return "[{}] - ({})".format(self.title, self.author)

class Catalog(db.Model):
    __tablename__ = 'catalog'
    id = db.Column(db.Integer, primary_key=True)
    room = db.Column(db.String(50))
    title = db.Column(db.String(100))
    txtid = db.Column(db.Integer)

    def __init__(self, title, uri, txtid):
        self.title = title
        self.room = uri
        self.txtid = txtid

    def __str__(self):
        return "[{}] - [{}]".format(self.txtid, self.title)


class Chapter(db.Model):
    __tablename__ = "chapter"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    chapter = db.Column(db.Integer)
    content = db.Column(db.Text)
    txtid = db.Column(db.Integer)

    def __init__(self, content, title, **kwargs):
        self.content = content
        self.title = title
        self.id = kwargs['id'] if 'id' in kwargs else None
        self.chapter = kwargs['chapter'] if 'chapter' in kwargs else None
        self.txtid = kwargs['txtid'] if 'txtid' in kwargs else None


    @classmethod
    def newc(cls, title, chapter, content, txtid):
        c = cls()
        c.title = title
        c.chapter = chapter
        c.content = content
        c.txtid = txtid
        return c

    def __repr__(self):
        return "[{}] - ({})".format(self.title, self.id)

    def __str__(self):
        return "[{}] - ({})".format(self.title, self.id)
