# -*- coding:utf-8 -*-
import os
import logging
import logging.handlers
 
class MyLogger(logging.Logger):
    def __init__(self, filename='log/test.log'):
        # super(MyLogger, self).__init__(filename)
        logging.Logger.__init__(self, filename)
 
        # 设置日志格式
        fmtHandler = logging.Formatter('[%(asctime)s][%(funcName)s][%(levelname)s]%(message)s')

        # 终端log输出流设置
        try:
            consoleHd = logging.StreamHandler()
            consoleHd.setLevel(logging.DEBUG)
            consoleHd.setFormatter(fmtHandler)
            self.addHandler(consoleHd)
        except Exception as reason:
            self.error("%s" % reason)
 
        # 设置log文件
        try:
            os.makedirs(os.path.dirname(filename))
        except Exception as reason:
            pass
            
        # try:
            # fileHd = logging.FileHandler(filename)
            # fileHd.setLevel(logging.DEBUG)
            # fileHd.setFormatter(fmtHandler)
            # self.addHandler(fileHd)
        # except Exception as reason:
            # self.error("%s" % reason)            
 
        # 设置回滚日志,每个日志最大10M,最多备份5个日志
        try:
            # rtfHandler = logging.BaseRotatingHandler(
                # filename, maxBytes=10*1024*1024, backupCount=5)
            rtfHandler = logging.handlers.RotatingFileHandler(
                filename, maxBytes=10*1024*1024, backupCount=5)
            rtfHandler.setLevel(logging.DEBUG)
            rtfHandler.setFormatter(fmtHandler)
        except Exception as reason:
            self.error("%s" % reason)
        else:
            self.addHandler(rtfHandler)
        return
if __name__ == "__main__":
    pass
