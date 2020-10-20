from django.urls import path
from Main import views

 
urlpatterns = [
    path('', views.index, name='home'),
    path('loadphoto/', views.loadphoto),
    path('users/', views.get_all_users),
]