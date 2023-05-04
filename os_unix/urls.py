from django.conf.urls import url
from os_unix import views
from django.urls import path

urlpatterns = [
    url(r'^os_unix/$', views.criminal_data),
    path('os_unix/<str:name>/', views.criminal_name),
    path('os_unix/<str:name>/update/', views.update_criminal),
]
