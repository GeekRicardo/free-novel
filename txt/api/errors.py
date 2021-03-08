#!/User/ricardo/anaconda3/bin/python
# -*- encoding: utf-8 -*-
'''
@File     :  errors.py
@Time     :  2020/10/23 16:48:22
@Author   :  Ricardo
@Version  :  1.0
@Desc     :  错误处理
'''

# import lib here
from flask import render_template
from txt.main import main


@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@main.app_errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500