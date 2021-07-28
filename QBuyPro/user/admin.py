from django.contrib import admin

# Register your models here.
from user.models import UserModel


class UserModelAdmin(admin.ModelAdmin):
    list_display = ('id','name','phone')
    fields = ('name','phone','auth_key')


admin.site.register(UserModel, UserModelAdmin)