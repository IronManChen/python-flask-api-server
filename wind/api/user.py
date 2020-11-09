#! /usr/bin/env python3
#! -*- coding:utf -*-

from flask import Blueprint, g, jsonify, request
from wind.controller.user import UserController
from wind.base import token_required, api_except, return_format

user_auth_api = Blueprint('user_auth_api',__name__)
@user_auth_api.route('/api/v1/user/userauth', methods=['POST'])
@api_except
def userauth():
    username = g.request_data['username']
    password = g.request_data['password']
    token = UserController.create_token(username, password)
    return return_format(data=token)


test_token_api = Blueprint('test_token_api',__name__)
@test_token_api.route('/api/v1/user/tokentest', methods=['POST'])
@api_except
@token_required
def tokentest():
    test = g.request_data['test']
    return return_format(data="ok")

