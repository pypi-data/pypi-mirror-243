# -*- coding: UTF-8 -*-
import logging
import logging.handlers 
from skywalking.trace.context import get_context
import datetime
from pytz import  timezone

cn = timezone('Asia/Shanghai')
def beijing(sec):
    return datetime.datetime.now(cn).timetuple()
logger = logging.getLogger()
#定义链路追踪过滤器
class TraceFilter(logging.Filter):
  traceId = ""
  def filter(self, record):
    record.traceId = getTraceId()
    return True
## 获取链路追踪id
def getTraceId():
     return str(get_context().segment.related_traces[0])

#链路追踪类
class TraceLog(object):
  """
  日志记录
  """
  def __init__(self):
    self.logger =  logging.getLogger()
    self.logger.setLevel(logging.INFO)
    self.logger.propagate = False
    self.filter_ = TraceFilter()
    self.logger.addFilter(self.filter_)
    formatter = logging.Formatter("[%(traceId)s]-%(asctime)s %(name)s %(filename)s  %(levelname)s %(message)s")
    formatter.converter = beijing
    self.formatter = formatter
  def console(self, level, message):

    # 创建一个StreamHandler,用于输出到控制台
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(self.formatter)
    self.logger.addHandler(ch)

    if level == 'info':
      self.logger.info(message)
    elif level == 'debug':
      self.logger.debug(message)
    elif level == 'warning':
      self.logger.warning(message)
    elif level == 'error':
      self.logger.error(message)
    # 这两行代码是为了避免日志输出重复问题
    self.logger.removeHandler(ch)

  def debug(self, message):
    self.console('debug', message)

  def info(self, message):
    self.console('info', message)

  def warning(self, message):
    self.console('warning', message)

  def error(self, message):
    self.console('error', message)