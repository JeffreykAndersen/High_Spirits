from django.urls import path
from . import views

urlpatterns = [
    path('', views.log_page),
    path('register_user', views.register_user),
    path('log_in', views.log_in),
    path('logged_in', views.logged_in),
    path('log_out', views.logout)
]
