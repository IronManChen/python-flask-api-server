#! /usr/bin/env python3
#! -*- coding:utf -*-

from wind.controller import ControllerBase
from wind.dao.user import UserDao
from wind.exception import AuthError
from oslo_config import cfg
from oslo_log import log
import uuid 

CONF = cfg.CONF
LOG = log.getLogger(__name__)

class UserController(ControllerBase):
    def __init__(self):
        super(UserController, self).__init__()
        self.userdb = UserDao()

    @classmethod
    def create_token(cls, username, password):
        userdata = cls().userdb.user_auth(username, password)
        if len(userdata) == 0:
            LOG.error("用户: {0} 认证失败".format(username))
            raise AuthError
        else:
            token = uuid.uuid4().hex
            cls().userdb.token_save(token, username)
            LOG.info("用户: {0} 认证成功, 获取 Token: {1}".format(username, token))
            return token

    def get_user_by_token(self, token):
        username = self.userdb.get_token(token)
        if len(username) == 0:
            raise AuthError
        else:
            return username[0]['username']
