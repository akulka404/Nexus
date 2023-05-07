from django.conf.urls import url
from cred_verify import views
from django.urls import path

urlpatterns = [
    url(r'^cred_verify/$', views.criminal_data),
    path('cred_verify/<str:name>/', views.criminal_name),
]
