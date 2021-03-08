#!/User/ricardo/anaconda3/bin/python
# -*- encoding: utf-8 -*-
'''
@File     :  views.py
@Time     :  2020/10/23 16:50:26
@Author   :  Ricardo
@Version  :  1.0
@Desc     :  主控制类
'''

# import lib here
from flask import Flask, request, render_template, make_response, send_from_directory, redirect, url_for, session, jsonify, Response
from flask import current_app

from txt.api import api
from txt import db, redis
from txt.models import User, Chapter, TXT
from txt.spiders.xsbiqugeSpider import XBQGSpider

xbqgSpider = XBQGSpider()

@api.route('/', methods=['GET', 'POST'])
def index():
    """
    test
    ---
    tags:
        - test
    description:
        测试使用，你可以请求这个看一下是我的问题还是你的问题
    parameters:

    """
    return render_template('index.html')


@api.route('/search', endpoint='searchTxt', methods=['GET', 'POST'])
def searchTxt():
    """
    搜索小说
    ---
    tags:
        - txt
        - api
    description:
        - 传来要搜索的title，给你返回搜到的小说，一般来说名字需要比较准确
    parameters:
        - name: body
          in: body
          required: true
          schema:
            id: 搜索小说
            required:
              - title
            properties:
              title:
                type: string
                decription: 要搜索的小说名
    responses:
      200:
          description: 成功
          example: {
            "code": 0,
            "data": [
                {
                    'author': 作者,
                    'desc': 简介,
                    'lastc': 最新一章,
                    'title': 小说名,
                    'updatetime': 更新时间,
                    'url': 小说的id
                },
            ],
            'title': 你搜索的小说名
          }
    """
    title = request.form.get('title') or request.args.get('title')
    current_app.logger.info("search:"+ title)
    if title:
        results = xbqgSpider.search(title)
        if results:
            return jsonify({
                "code":0,
                "data": results,
                "title": title
            })
        else:
            return jsonify({
                "code": -1,
                "msg": "没有搜到东西！"
            })
    else:
        return jsonify({
                "code": -2,
                "msg": "参数填错了呀傻逼！"
            })


@api.route('/getcatalog/<room>', endpoint='getcatalog', methods=['GET', 'POST'])
def getcatalog(room):
    if not room:
        return jsonify({
            "code": -2,
            "msg": "参数都是空的你查个毛啊！"
        })
    maininfo, catalogs = xbqgSpider.getcatalogs(room)
    if catalogs:
        return jsonify({
            'code': 0,
            "data": {
                "maininfo": maininfo,
                "catalogs": catalogs,
                "room": room
            },
            "from": xbqgSpider.BaseURL
        })
    else:
        return jsonify({
            "code": -1,
            "msg": "这回是在下输了，没有搜到东西！"
        })


@api.route('/content/<room>/<chapter>', endpoint='getcontent', methods=['GET', 'POST'])
def getcontent(room, chapter):
    title, content = xbqgSpider.getContent(room, chapter)
    if room and chapter:
        return jsonify({
            "code": 0,
            "data": {
                "title": title,
                "content": content
            }
        })
    else:
        return jsonify({
            "code": -2,
            "msg": "不告诉我哪章我还能给你编出来吗！"
        })



def login_require(func):
    """
    登录校验装饰器
    """
    is_login_require = True
    def decorator(*args, **kwargs):
        if is_login_require:
            # 现在是模拟登录，获取用户名，项目开发中获取session
            username = session.get('username', None) or request.cookies.get('username')
            user = db.session.query(User).filter_by(username=username).first()
            # 判断用户名存在且用户名是什么的时候直接那个视图函数
            if user.username:
                return func(*args, **kwargs)
            else:
                # 如果没有就重定向到登录页面
                return redirect(url_for("api.login"))

        else:
            return func(*args, **kwargs)
# decorator.__name__ = func.__name__
    return decorator

