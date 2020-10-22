# from rest_framework.routers import DefaultRouter
# from Main.views import UserViewSet


# router = DefaultRouter()
# router.register('users', UserViewSet)
 
# urlpatterns = router.urls

from django.urls import path
from .views import authentication
 
urlpatterns = [
    path('', authentication),
    # path('auth/', include('djoser.urls')),
]