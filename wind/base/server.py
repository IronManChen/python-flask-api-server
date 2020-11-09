#! /usr/bin/env python3
#! -*- coding:utf-8 -*-




from flask import Flask, request, g, session
import datetime
import json
import os

from wind.api.user import user_auth_api, test_token_api
import pbr.version
import eventlet
from eventlet import wsgi
from wind import config
from oslo_config import cfg


CONF = cfg.CONF
_APP = None

MODULES = [
    (user_auth_api,''),
    (test_token_api,''),
]

def configure_app(app):
    pass

def configure_logging(app):
    pass

'''
蓝本注册管理
'''
def configure_blueprints(app,modules):
    for module, url_prefix in modules:
        app.register_blueprint(module, url_prefix=url_prefix)


def configure_exception_pages(app):
    pass

'''
创建app，指定一些静态文件和模板的路径
'''
def make_app(do_config=False):
    global _APP
    if _APP and do_config is False:
        return _APP

    app = Flask(__name__)
    app.config['MAX_CONTENT_LENGTH'] = 1024000000
    app.secret_key = 'saaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'

    if do_config:
        configure_app(app)
        configure_logging(app)
        configure_blueprints(app, MODULES)
        configure_exception_pages(app)

    _APP = app
    return app

app = make_app()

def before_run(possible_topdir="", conf_dir="etc", conf_file="wind.conf"): 
    dev_conf = os.path.join(possible_topdir,
                            conf_dir,
                            conf_file)

    config_files = None 
    if os.path.exists(dev_conf): 
        config_files = [dev_conf]

    config.configure(
        version = pbr.version.VersionInfo("wind").version_string(), 
        config_files=config_files,
    )

    app = make_app(do_config=True)
    app._static_folder = os.path.join(possible_topdir, "wind", "static")

    app.permanent_session_lifetime = datetime.timedelta(days=1)
    
    @app.before_request 
    def before_request():
        session.permanent = True
    
    @app.errorhandler(404) 
    def page_not_found(error):
        return json.dumps(dict(msg=u"请求的服劳地址不存在")), 404
    
    @app.errorhandler(405) 
    def page_not_found(error):
        return json.dumps(dict(msg=u"请求的服务地址方法不存在")), 405

    @app.before_request 
    def before_request():
        try: 
            g.request_data = {}

            if request.data is not None and request.data != "":
                g.request_data = json.loads(request.data)
            else:
                for k, v in request.values:
                    g.request_data[k] = v
        except :
            return json.dumps(dict(msg="谓求报文格式错误,需要保证报文的格式为JSON格式.")), 400
    return app

def run(possible_topdir="", conf_dir="etc", conf_file="wind.conf"): 
    app = before_run(possible_topdir, conf_dir, conf_file) 
    eventlet.patcher.monkey_patch(os=False, select=True, socket=True, thread=False, time=True, psycopg=False, MySQLdb=False)
    wsgi.server(eventlet.listen(('', int(CONF.server.port))), app)   
