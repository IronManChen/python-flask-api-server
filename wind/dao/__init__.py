#! /usr/bin/env python3
#! -*- coding:utf-8 -*-

from wind.utils.mysql import DB
from oslo_config import cfg
CONF = cfg.CONF

class WindDaoBase():
    def __init__(self):
        self.host = CONF.mysql.windhost       
        self.port = CONF.mysql.windport             
        self.username = CONF.mysql.windusername 
        self.password = CONF.mysql.windpassword 
        self.schema = CONF.mysql.windschema       
        self.db = DB(self.host, self.port, self.username, self.password, self.schema)
