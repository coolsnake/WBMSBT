#coding=utf-8
import datetime

import tornado.web
import tornado.options

import weblog
from database.db_config import db_session
from database.tbl_admin import TblAdmin
class BaseHandler(tornado.web.RequestHandler):
    localStore = {}

    def initialize(self):
        pass

    # def __init__(self, *argc, **argkw):
        """
        定义 handler 的 session, 注意，根据 HTTP 特点.
        每次访问都会初始化一个 Session 实例哦，这对于你后面的理解很重要
        """
        self.localVariable = {}
        self.initLocalVariable()
        self.browsing_history()
        # super(BaseHandler, self).__init__(*argc, **argkw)

    def mysqldb(self):
        return db_session

    def on_finish(self):
        self.mysqldb().close()

    def get_current_user(self):
        # self.set_secure_cookie("user_account","TestAccount")
        # return self.get_secure_cookie("user_account")
        if self.get_secure_cookie("user_account") is not None:
            return self.get_secure_cookie("user_account")
        else:
            return "TestAccount"

    def initLocalVariable(self):
        variables = self.mysqldb().query(TblAdmin).all()
        for var in variables:
            if var.name not in self.localVariable.keys():
                self.localVariable[var.name] = var.value

    def browsing_history(self):
        login_name = self.get_current_user()

        if login_name is None:
            return
        try:
            self.mysqldb().execute(
                "INSERT INTO tbl_browsing_history (user_ip,user_account,request_method,"
                "uri,status,browsing_date,browsing_time,user_agent) "
                "VALUES(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\');"
                %(self.request.remote_ip, login_name, self.request.uri,self.request.method,
                  self.get_status(),datetime.datetime.now().strftime('%Y%m%d'),
                  datetime.datetime.now().strftime('%H%M%S'), self.request.headers.get("User-Agent"))
            )
            self.mysqldb().commit()
        except:
            weblog.exception("BaseHandler:visit_history error")
            self.mysqldb().rollback()

