# --coding:utf-8--
from django.urls import path
from . import views

app_name = 'stockapp'
urlpatterns = [
    path('stocks/<stock_id>/', views.StockView.as_view(), name='stocks'),
    path('goods/<wd>/', views.GoodsView.as_view(), name='goods'),
    path('query/<wd>/',views.QueryView.as_view(),name='query')
]