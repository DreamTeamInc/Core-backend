# from rest_framework.routers import DefaultRouter
from django.urls import path
from Main.views import *


# router = DefaultRouter()
# router.register('users', UserViewSet)

# urlpatterns = router.urls


urlpatterns = [
    path('users/create/', CreateVUser.as_view()),
    path('users/all/', GetAllUsers.as_view()),
    path('users/<int:pk>/', PutGetDeleteOneUser.as_view()),
    path('auth/', authentication),
    path('locations/all', GetAllLocations.as_view()),
    path('locations/<int:pk>/', PutGetDeleteOnePhoto.as_view()),
    path('locations/create', CreatePhoto.as_view()),
    path('wells/all', AllWells.as_view()),
    path('wells/<location>', WellInLocation.as_view()),
]
