#!/User/ricardo/anaconda3/bin/python
# -*- encoding: utf-8 -*-
'''
@File     :  __init__.py
@Time     :  2020/10/23 16:45:11
@Author   :  Ricardo
@Version  :  1.0
@Desc     :  主应用，主路由
'''

# import lib here
from flask import Blueprint

main = Blueprint('main', __name__)

from txt.main import views, errors