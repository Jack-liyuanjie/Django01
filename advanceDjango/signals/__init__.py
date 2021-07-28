# --coding:utf-8--
from django import dispatch

# 定义信号
codeSignal = dispatch.Signal(providing_args=['path',
                                             'phone',
                                             'code'])


