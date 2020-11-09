#! /usr/bin/env python3
#! -*- coding:utf-8 -*-

from wind.dao import WindDaoBase

class UserDao(WindDaoBase):
    def __init__(self):
        super(UserDao, self).__init__()

    def user_auth(self, username, password):
        with self.db as db:
            sql = "select username, password from USER where username = \"{0}\" and password = MD5(\"{1}\")".format(username,password)
            db.execute(sql)
            data = db.fetchall()
            return data

    def token_save(self,token, username):
        with self.db as db:
            sql = "insert into TOKENS(token,username,expire_time) values (\"{0}\",\"{1}\",date_sub(NOW(),interval -1 day));".format(token,username)
            db.execute(sql)
                
    def get_token(self, token):
        with self.db as db:
            sql = "select username from TOKENS where token=\"{0}\";".format(token)
            db.execute(sql)
            data = db.fetchall()
            return data
    
