from django.contrib import admin
from orderapp.models import OrderModel


# Register your models here.
class OrderAdmin(admin.ModelAdmin):
    list_display = ('num', 'title', 'status', 'pay_type', 'receiver', 'receiver_phone', 'receiver_address','price')
    fields = ('price','num', 'title', 'status', 'pay_type', 'receiver', 'receiver_phone', 'receiver_address')
    list_filter = ('status',)


admin.site.register(OrderModel, OrderAdmin)
