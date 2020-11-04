from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from Main.views import *


urlpatterns = [
    path('users/create/', CreateUser.as_view()),
    path('users/all/', GetAllUsers.as_view()),
    path('users/<int:pk>/', PutGetDeleteOneUser.as_view()),
    path('auth/', authentication),
    path('locations/all/', GetAllLocations.as_view()),
    path('wells/all/', AllWells.as_view()),
    path('wells/<location>/', WellInLocation.as_view()),
    path('mask/create/', CreateMask.as_view()),
    path('mask/all/', GetAllMasks.as_view()),
    path('mask/<int:pk>/', PutGetDeleteOneMask.as_view()),
    path('model/create/', CreateModel.as_view()),
    path('model/all/', GetAllModels.as_view()),
    path('model/<int:pk>/', PutGetDeleteOneModel.as_view()),
    path('photo/all/', GetAllPhotos.as_view()),
    path('photo/<int:pk>/', PutGetDeleteOnePhoto.as_view()),
    path('photo/create/', CreatePhoto.as_view()),
    path('photo/<int:pk>/masks/', AllMaskByPhoto.as_view()),
    path('photo/<int:pk>/like_mask/<int:mask_id>/', GiveLike),
    path('photo/<int:pk>/dislike_mask/<int:mask_id>/', DisLike),
    path('users/<int:pk>/model/all/', GetAllModelsByUser.as_view()),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
