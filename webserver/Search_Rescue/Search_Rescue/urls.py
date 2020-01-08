"""Search_Rescue URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path
from django.conf.urls import url, include

# 引入权限验证
from rest_framework.authtoken import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # TODO:[*] 20-01-07 引入drf的权限认证
    path('api-auth/', include('rest_framework.urls')),
    path('api-token-auth/', views.obtain_auth_token),
    url('^rescue/', include(('rescue.urls', "rescue"), namespace="rescue")),
    url('^oilspilling/', include(('oilspilling.urls', "oilspilling"), namespace="oilspilling")),
]
