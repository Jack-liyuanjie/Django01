from signals import codeSignal
from django import dispatch


# 接信号
@dispatch.receiver(codeSignal)
def cache_code(sender, **kwargs):
    print('dispatch.receiver<cache_code>')
    print(sender, kwargs)
