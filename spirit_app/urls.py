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
    path('edit_alcohol/<int:id>', views.edit_alcohol),
    path('alcohol_edit_confirm/<int:id>', views.alcohol_edit_confirm),
    path('your_bar', views.your_bar),
    path('adding_to_bar/<int:id>', views.adding_to_bar),
    path('remove_from_bar/<int:id>', views.remove_from_bar),
    # COCKTAIL CREATION MANAGMENT
    path('codex', views.codex),
    path('create_cocktail', views.create_cocktail),
    path('cocktail_add', views.cocktail_add),
    path('remove_cocktail/<int:id>', views.delete_cocktail),
    path('edit_cocktail/<int:id>', views.edit_cocktail),
    path('cocktail_edit_confirm/<int:id>', views.cocktail_edit_confirm),
    path('view_cocktail/<int:id>', views.view_cocktail),
]
