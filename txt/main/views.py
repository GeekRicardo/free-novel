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
from flask import request, render_template, make_response, send_from_directory, redirect, url_for, session, jsonify, Response
from flask import current_app

from txt.main import main
from txt import db, redis, cache
from txt.models import User, Chapter, TXT, Catalog
from txt.spiders import xsbiqugeSpider
from txt.spiders.xsbiqugeSpider import XBQGSpider

xbqgSpider = XBQGSpider()

@main.route('/', methods=['GET', 'POST'])
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
    txts = db.session.query(TXT.id, TXT.title, TXT.author, TXT.curr, TXT.url)
    # curr = getcatabyspider()
    return render_template('index.html', txts = txts)


@main.route('/search', endpoint='searchTxt', methods=['GET', 'POST'])
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
    if request.method == 'GET':
        return render_template('search.html')
    else:
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


@main.route('/catalog/<room>', endpoint='getcatalog', methods=['GET', 'POST'])
def getcatalog(room):
    txt = db.session.query(TXT).filter_by(url=room).first()
    if txt:
        catalogs = db.session.query(Catalog.room, Catalog.title).filter_by(txtid=room)
        # history = redis.get(str(room))
        c = [(cl.title.strip(), cl.room) for cl in catalogs]
        if request.method == 'GET':
            return render_template('owllook.html', room=room, catalogs=c, maininfo={
                'title': txt.title,
                'author': txt.author,
                'img': ''
            }, self='True')
        else:
            return jsonify({
                'catalogs': c
            })
    else:
        maininfo, catalogs = xbqgSpider.getcatalogs(room)
        current_app.logger.info('add txt:'+maininfo['title'])
        newtxt = TXT(maininfo['title'], maininfo['author'], room)
        db.session.add(newtxt)
        db.session.commit()
        for c in catalogs:
            # print(c)
            title, uri = c
            catalog = Catalog(title, uri, newtxt.id)
            db.session.add(catalog)
            db.session.commit()
        if request.method == 'GET':
            return render_template('owllook.html', room=room, catalogs=catalogs, maininfo={
                'title': newtxt.title,
                'author': newtxt.author,
                'img': ''
            }, self='True')
        else:
            return jsonify({
                'catalogs': catalogs
            })

    return render_template('index.html', msg='无此小说')


@cache.memoize()
def getcatabyspider(room):
    return xbqgSpider.getcatalogs(room)




@main.route('/content/<room>/<chapterid>', endpoint='getcontent', methods=['GET', 'POST'])
def getcontent(room, chapterid):
    chapter = None
    # chapter = db.session.query(Chapter).filter_by(txtid=room, id=chapterid).first()
    chapter = xbqgSpider.getContent(room, chapterid)
    maininfo, catalogs = getcatabyspider(room)
    currc_index = [i[1] for i in catalogs].index(chapterid)

    # 更新进度
    if chapter:
        txt = db.session.query(TXT).filter_by(url=room).first()
        txt.curr = chapterid
        db.session.commit()

    if request.method == 'POST':
        if not chapter[1]:
            return jsonify({
                'code': -1,
                'msg': "有点bug，等会修复一下..."
            })
        # print(chapter)
        return jsonify({
            'code': 0,
            'data':{
                'room': room,
                'title': chapter[0],
                'content': chapter[1],
                "prec": catalogs[currc_index - 1],
                "nextc": catalogs[currc_index + 1]
            }
        })
    else:
        if chapter[1]:
            c = Chapter(content=chapter[1], title=chapter[0], id=-1, txtid=room)
            # chapter.content = chapter.content.split('\n')
            isScroll = request.cookies.get('play') or 'stop'
            isDay = request.cookies.get('isDay') or 'night'
            fontsize = request.cookies.get('size') or '16'
            return render_template('chapter.html', chapter=c, isDay=isDay, fontsize=fontsize, play=isScroll, prec=catalogs[currc_index - 1], nextc=catalogs[currc_index + 1])
            # return render_template('index.html')
        else:
            return redirect(url_for('main.index'))



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
                return redirect(url_for("main.login"))

        else:
            return func(*args, **kwargs)
# decorator.__name__ = func.__name__
    return decorator

