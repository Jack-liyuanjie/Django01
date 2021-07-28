from django.contrib import admin

from mainapp.models import UserEntity, FruitEntity, CateTypeEntity, StoreEntity, RealProfile, CartEntity, \
    FruitCartEntity, TagEntity


# Register your models here.

class UserAdmin(admin.ModelAdmin):
    # 后台显示字段的行列
    list_display = ('id', 'name', 'phone')
    # 分页设置每页显示2条
    list_per_page = 2
    # 过滤器，一般来配置分类字段
    list_filter = ('id', 'phone')
    # 搜索字段
    search_fields = ('id', 'phone')


class CateTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'order_num')


class FruitAdmin(admin.ModelAdmin):
    list_display = ('name', 'source', 'price', 'category', 'fruit_picture')
    fields = ('name', 'source', 'price', 'category', 'fruit_picture','users','tags')


class StoreAdmin(admin.ModelAdmin):
    list_display = ('id_', 'name', 'city', 'address', 'store_type', 'logo', 'create_time')
    # 指定表单修改的字段
    fields = ('name', 'city', 'address', 'store_type', 'logo', 'summary')


class RealProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'real_name', 'number', 'real_type')


class CartEntityAdmin(admin.ModelAdmin):
    list_display = ('user', 'no')


class FruitCartEntityAdmin(admin.ModelAdmin):
    # 显示字段可以引用关系实体对象的属性
    list_display = ('cart', 'fruit', 'price1_title', 'cnt', 'price_title')

    def price1_title(self, obj):
        return obj.price1

    def price_title(self, obj):
        return obj.price

    price1_title.short_description = '单价'
    price_title.short_description = '小计'


class TagEntityAdmin(admin.ModelAdmin):
    list_display = ('name', 'order_num')
    fields = ('name', 'order_num')


# 将模型增加到站点中
admin.site.register(UserEntity, UserAdmin)
admin.site.register(CateTypeEntity, CateTypeAdmin)
admin.site.register(FruitEntity, FruitAdmin)
admin.site.register(StoreEntity, StoreAdmin)
admin.site.register(RealProfile, RealProfileAdmin)
admin.site.register(CartEntity, CartEntityAdmin)
admin.site.register(FruitCartEntity, FruitCartEntityAdmin)
admin.site.register(TagEntity, TagEntityAdmin)
