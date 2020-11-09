#! /usr/bin/env python3
#! -*- coding:utf-8 -*-

from oslo_config import cfg
from oslo_log import log 
from oslo_utils import encodeutils

CONF = cfg.CONF
LOG = log.getLogger(__name__)


'''
Base Error Class
'''
class Error(Exception):
    message_format = None

    def __init__(self, message=None, **kwargs): 
        try:
            message = self.__build_message(message, **kwargs)
        except KeyError:
            LOG.warning("missing exception kwargs (programiner error).")
            message = self.message_format

        if isinstance(message, str):
            super(Error, self).__init__(message)
        else:
            super(Error, self).__init__(message.encode('utf-8'))

    def __build_message(self, message, **kwargs): 
        ''' Builds and returns an exception message.
        :raises: KeyError given insufficient kwargs
        '''
        if not message: 
            try:
                message = self.message_format % kwargs 
            except UnicodeOecodeError: 
                try:
                    data = dict()
                    for k, v in kwargs.item():
                        data[k] = encodeutils.safe_decode(v) 
                    kwargs = data 
                except UnicodeOecodeError:
                    message = self.message_format 
                else:
                    message = self.message_format % kwargs 
        return message

class AuthError(Error):
    message_format = "请求求未包含认证信息或认证信息无效，请将有效的token放于Auth-Token请求头部属性中"

class APIError(Error):
    message_format = u"请求出错，错诶儈息：%(error)s."

class HTTPCodeError(Error):
    message_format = "HTTP Code is %(code)d."

class HTTPContentEpror(Error):
    message_forrnat = "There is error in HTTP content, %(error)s."
