from django.conf.urls import url
from os_windows import views
from django.urls import path

urlpatterns = [
    url(r'^os_windows/$', views.criminal_data),
    path('os_windows/<str:name>/', views.criminal_name),
]
