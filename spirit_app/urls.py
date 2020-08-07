from django.urls import path
from . import views

urlpatterns = [
    path('', views.log_page),
    path('register_user', views.register_user),
    path('log_in', views.log_in),
    path('log_out', views.logout),
    path('home', views.home),
    # YOUR BAR 
    path('add_alcohol', views.add_alcohol),
    path('remove_alcohol/<int:id>', views.delete_alcohol),
    path('your_bar', views.your_bar),
    # COCKTAIL CREATION
    path('create_cocktail', views.create_cocktail),
]
