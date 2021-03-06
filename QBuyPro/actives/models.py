from django.db import models

# Create your models here.
from goods.models import GoodsModel


class ActiveModel(models.Model):
    title = models.CharField(max_length=50,
                             verbose_name='名称')

    img1 = models.ImageField(verbose_name='图片1',
                             upload_to='actives')

    start_time = models.CharField(max_length=30,
                                  verbose_name='开始时间')

    end_time = models.CharField(max_length=30,
                                verbose_name='结束时间')

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'app_active'
        verbose_name_plural = verbose_name = '活动信息'


class ActiveGoodsModel(models.Model):
    active = models.ForeignKey(ActiveModel,
                               verbose_name='活动名',
                               related_name='activies',
                               null=True,
                               on_delete=models.SET_NULL)

    goods = models.ForeignKey(GoodsModel,
                              related_name='activies',
                              verbose_name='商品名',
                              null=True,
                              on_delete=models.SET_NULL)

    rate = models.FloatField(verbose_name='折扣率',
                             default=.88)

    @property
    def rate_price(self):
        return float(self.goods.price)*self.rate

    def __str__(self):
        return self.active.title + ":" + self.goods.name

    class Meta:
        db_table = 'app_active_goods'
        verbose_name_plural = verbose_name = '活动详情'