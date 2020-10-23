# from rest_framework.routers import DefaultRouter
from django.urls import path
from Main.views import *


# router = DefaultRouter()
# router.register('users', UserViewSet)

# urlpatterns = router.urls


urlpatterns = [
    path('users/create/', UserCreateView.as_view()),
    path('users/all/', UserListView.as_view()),
    path('users/detail/<int:pk>/', UserDetailView.as_view()),
    path('auth/', authentication),
    # path('auth/', include('djoser.urls')),
]
