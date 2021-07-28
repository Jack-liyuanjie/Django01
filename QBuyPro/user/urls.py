# --coding:utf-8--
from django.urls import path
from . import views
from .views import user_api, user_api_detail, UserAPIView, UserAPIDetailView

app_name = 'user'
urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('api/', UserAPIView.as_view(), name='api'),
    path('api/<int:pk>', UserAPIDetailView.as_view(), name='api-detail'),
    # path('api/<int:pk>',user_api_detail,name='api-detail'),
]
