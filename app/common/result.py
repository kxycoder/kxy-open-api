#!/usr/bin/python
# -*- coding:utf-8 -*-
"""
__auth__ = liujiguo
__date__ = 2018/12/20 19:59
__soft__ = vscode
"""
import traceback
from kxy.framework.kxy_logger import KxyLogger
logger = KxyLogger.getLogger(__name__)
from kxy.framework.context import trace_id

class Result:
    def errorcode(code:int,msg):
        return {
            'status': False,
            'status_code': code,
            'error': msg
        }
    @staticmethod
    def friendlyerror(msg):
        if msg == 'server-error':
            msg = "服务器端发生异常，工程师正在抢修..."
        return {
            'status': False,
            'code': 40000,
            'error': msg
        }

    @staticmethod
    def error(error:str='',errcode:int=500):
        logger.error(error)
        if errcode == 0:
            raise Exception('错误的code必须大于0')
        traceId = trace_id.get()
        return {
            'code': errcode,
            'msg': error,
            'traceId': traceId
        }

    @staticmethod
    def error401():
        return {
            'status': False,
            'code': 401,
            'msg': "请重新登录"
        }
    @staticmethod
    def error501(msg):
        # logger.error(msg)
        return {
            'status': False,
            'code': 501,
            'msg': msg
        }

    @staticmethod
    def success(data):
        return {
            'code':0,
            'msg':'',
            'data': data
        }

    @staticmethod
    def pagesuccess(data, count):
        return {
            'code': 0,
            'data': {'list':data,'total':count}
        }