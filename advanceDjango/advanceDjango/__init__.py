from __future__ import absolute_import, unicode_literals
import pymysql
from django.db.models.signals import pre_delete, post_delete, pre_save, post_save
from django.dispatch import receiver

pymysql.install_as_MySQLdb()


# 定义一个模型操作类删除前的信号
def model_delete_pre(sender, **kwargs):
    from user.models import Order
    # sender 表示 哪一个Model的对象将要被删除 信号发送者
    # kwargs 表示信号的基本信息，信号发送时，传递的一些信息
    # print(sender)   # models.Model的子类
    # print(kwargs)   # key:signal,instance,using
    info = 'Prepare.Delete %s 类的 id=%s,title=%s'
    # print(issubclass(sender, Order))  # True
    # print(isinstance(sender,Order))  # False
    # print(sender is Order)  # True
    # print(sender == Order)  # True
    if sender == Order:
        print(info % ('订单模型',
                      kwargs.get('instance').id,
                      kwargs.get('instance').title))


@receiver(post_delete)
def dele_model_post(sender, **kwargs):
    print(sender, '删除成功', kwargs)


# 连接信号
pre_delete.connect(model_delete_pre)


# post_delete.connect(dele_model_post)


def pre_save_model(sender, **kwargs):
    from user.models import Order
    info = ' 正在增加Order模型类的信息 id=%s,title=%s'
    if sender == Order:
        print(info % (kwargs.get('instance').id,
                      kwargs.get('instance').title))


def post_save_model(sender, **kwargs):
    print(sender, '添加成功', kwargs)


pre_save.connect(pre_save_model)
post_save.connect(post_save_model)



from .celery import app as celery_app

# 向项目模块中增加celery_app对象
__all__ = ('celery_app',)
