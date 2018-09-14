# -*- coding: UTF-8 -*-
# db util
# 数据库读取
import sqlite3


class DBUtil(object):

    def __init__(self):
        self.conn = sqlite3.connect('config.db')
