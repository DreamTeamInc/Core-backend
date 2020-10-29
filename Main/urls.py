from django.urls import path
from Main.views import *


urlpatterns = [
    path('users/create/', CreateUser.as_view()),
    path('users/all/', GetAllUsers.as_view()),
    path('users/<int:pk>/', PutGetDeleteOneUser.as_view()),
    path('auth/', authentication),
    path('locations/all/', GetAllLocations.as_view()),
    path('locations/<int:pk>/', PutGetDeleteOnePhoto.as_view()),
    path('locations/create/', CreatePhoto.as_view()),
    path('wells/all/', AllWells.as_view()),
    path('wells/<location>/', WellInLocation.as_view()),
    path('mask/create/', CreateMask.as_view()),
    path('mask/all/', GetAllMasks.as_view()),
    path('mask/<int:pk>/', PutGetDeleteOneMask.as_view()),
    path('model/create/', CreateModel.as_view()),
    path('model/all/', GetAllModels.as_view()),
    path('model/<int:pk>/', PutGetDeleteOneModel.as_view()),
    path('photo/<int:pk>/masks/', AllMaskByPhoto.as_view()),
    path('photo/<int:pk>/like_mask/<int:mask_id>', GiveLike),
    path('photo/<int:pk>/dislike_mask/<int:mask_id>', DisLike),

]
