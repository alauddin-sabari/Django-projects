from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('item/new/', views.create_item, name='create_item'),
    path('item/<int:pk>/edit/', views.update_item, name='update_item'),
    path('item/<int:pk>/delete/', views.delete_item, name='delete_item'),
]