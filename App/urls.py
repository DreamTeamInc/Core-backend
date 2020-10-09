from django.contrib import admin
from django.urls import path
from Main import views
 
urlpatterns = [
    path('', views.index, name='home'),
    path('loadphoto/', views.loadphoto),
    path('admin/', admin.site.urls),
]