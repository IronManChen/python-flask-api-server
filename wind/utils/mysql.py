#! /usr/bin/env python3
#! -*- coding:utf-8 -*-

import MySQLdb
from oslo_config import cfg

CONF = cfg.CONF

MYSQL_DATETIME_FMT = "%Y-%m-%d %H:%M:%S"

class DB():
    def __init__(self,host, port, username, password, schema):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.schema = schema

    def __enter__(self):
        self.conn = None
        self.cursor = None
        try:
            self.conn = MySQLdb.connect(host=self.host,
                                        port=int(self.port),
                                        user=self.username,
                                        passwd=self.password,
                                        db=self.schema,
                                        charset='utf8',
                                        connect_timeout=5)
            self.conn.autocommit(False)
            self.cursor = self.conn.cursor(MySQLdb.cursors.DictCursor)
        except Exception as e:
            logger.exception(e)
        finally:
            return self.cursor
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            if self.conn:
                self.conn.commit()
        except Exception as e:
            logger.exception(e)

        try:
            if self.cursor:
                self.cursor.close()
        except Exception as e:
            logger.exception(e)

        try:
            if self.conn:
                self.conn.close()
        except Exception as e:
            logger.exception(e)
