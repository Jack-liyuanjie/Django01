from django.contrib import admin

# Register your models here.
from goods.models import GoodsModel


class GoodsModelAdmin(admin.ModelAdmin):
    list_display = ('id','name','price','img1','info')


admin.site.register(GoodsModel,GoodsModelAdmin)