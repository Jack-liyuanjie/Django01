"""QBuyPro URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.shortcuts import render
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from api import api_router


def Token_to(request):
  return render(request,'index.html')


urlpatterns = [
  path('admin/', admin.site.urls),
  path('active/', include('actives.urls', namespace='actives')),
  path('user/', include('user.urls', namespace='user')),
  path('api/', include(api_router.urls)),
  path('api-auth/', include('rest_framework.urls')),
  path('',Token_to)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
