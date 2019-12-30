from django.conf.urls import url, include
from django.urls import path
from Main import views

app_name = 'tasks'
urlpatterns = [
    path('test/', views.test)

]
