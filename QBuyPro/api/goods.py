# --coding:utf-8--
from rest_framework import serializers, viewsets
from goods.models import GoodsModel


# 序列化
class GoodsModelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GoodsModel
        fields = ('id', 'name', 'price', 'info', 'img1')


# api视图类
class GoodsAPIView(viewsets.ModelViewSet):
    queryset = GoodsModel.objects.all()
    serializer_class = GoodsModelSerializer
