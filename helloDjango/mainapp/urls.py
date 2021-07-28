from django.urls import path
from mainapp.views import user_list, user_list3, add_user,update_user,delete_user,find_fruit,find_store,all_store,count_fruit
from mainapp.user_v import login

urlpatterns = [
    path('list', user_list3),
    path('add', add_user),
    path('update', update_user),
    path('delete', delete_user),
    path('fruit', find_fruit),
    path('store', find_store),
    path('store_all', all_store),
    path('fruit_count', count_fruit),
    path('login', login),
]
