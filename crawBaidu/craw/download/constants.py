# coding:utf8
import os
from random import choice
import json

def get_pwd():
    return os.getcwd()

def get_user_agent():
    return choice(USER_AGENTS)

USER_AGENTS = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
]

get_headers = {
    "User-Agent": get_user_agent(),
    }

