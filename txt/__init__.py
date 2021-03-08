#!/User/ricardo/anaconda3/bin/python
# -*- encoding: utf-8 -*-
'''
@File     :  __init__.py
@Time     :  2020/10/23 16:41:56
@Author   :  Ricardo
@Version  :  1.0
@Desc     :  程序工厂，用于产出不同目录的应用，使用【蓝图】对应不同的路由
'''

# import lib here
from sys import prefix
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_dropzone import Dropzone
from flask_caching import Cache
from flasgger import Swagger
from redis import Redis

from config import config

db = SQLAlchemy()
dropzone = Dropzone()
cache = Cache(config={
    "CACHE_TYPE":"filesystem",
    "CACHE_DIR": "cache"
    # "CACHE_REDIS_HOST":"localhost",
    # "CACHE_REDIS_PORT":6379,
    # "CACHE_REDIS_PASSWORD":"",
    # "CACHE_REDIS_DB":4
})

# redis
redis = Redis('localhost', db=7, decode_responses=True)

# swagger config
swagger_config = Swagger.DEFAULT_CONFIG
swagger_config['title'] = 'txt api 傻瓜式用法' # 配置大标题
swagger_config['description'] = 'txt api usage' # 配置公共描述内容
swagger_config['host'] = 'swagger.txt.sshug.cn' # 请求域名

# swagger_config['swagger_ui_bundle_js'] = '//unpkg.com/swagger-ui-dist@3/swagger-ui-bundle.js'
# swagger_config['swagger_ui_standalone_preset_js'] = '//unpkg.com/swagger-ui-dist@3/swagger-ui-standalone-preset.js'
# swagger_config['jquery_js'] = '//unpkg.com/jquery@2.2.4/dist/jquery.min.js'
# swagger_config['swagger_ui_css'] = '//unpkg.com/swagger-ui-dist@3/swagger-ui.css'


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    db.init_app(app)
    cache.init_app(app)
    dropzone.init_app(app)
    Swagger(app, config=swagger_config)
    # 附加路由和自定义的错误页面
    from txt.main import main as main_bluepoint
    app.register_blueprint(main_bluepoint, url_prefix='/')
    from txt.api import api as api_bluepoint
    app.register_blueprint(api_bluepoint, url_prefix='/api/v1.0/')

    return app
