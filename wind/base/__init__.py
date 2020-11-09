#!/usr/bin/env python3
#! -*- coding:utf-8 -*-

import json
from functools import wraps
from flask import request, g
from oslo_serialization import jsonutils
from oslo_log import log
from oslo_config import cfg
import wind.exception as exception
from wind.controller.user import UserController

LOG = log.getLogger(__name__)
CONF = cfg.CONF
'''
用于api的认证
'''
def token_required(f):
    @wraps(f)
    def _login_check(*args, **kwargs):
        if request.headers.get("Auth-Token", None) is None:
            raise exception.AuthError
        token = request.headers.get("Auth-Token", None)
        user = UserController.get_user_by_token(token)
        # 将用户信息存放到g里，方便后续使用
        g.current_user = user
        return f(*args, **kwargs)
    return _login_check


'''
api异常处理
'''
def api_except(f):
    @wraps(f)
    def _abort_check(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            try:
                LOG.exception(e)
            except:
                LOG.error(str(e))
            if isinstance(e, exception.APIError):
                return return_format(str(e), 400)
            return return_format(str(e), 500)
    return _abort_check


'''
对api返回做统一封装
'''
def return_format(data=None, code=200):
    result = dict(result="success")
    if code == 200 and data is not None:
        result['result'] = data
    if code != 200 and data is None:
        result['result'] = "failed"
    if code != 200 and data is not None:
        result['result'] = data
    try:
        return json.dumps(result), code
    except:
        class SmartEncoder(jsonutils.json.JSONEncoder):
            def default(self, obj):
                if not isinstance(obj, dict) and hasattr(obj, "iteritems"):
                    return dict(obj, iteritems())
                return super(SmartEncoder, self).default(obj)
        return jsonutils.dumps(result, cls=SmartEncoder), code

