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
    path('user/<int:user_id>/photo/<int:pk>/like_mask/<int:mask_id>/', like),
    path('user/<int:user_id>/photo/<int:pk>/dislike_mask/<int:mask_id>/', disike),
    path('users/<int:pk>/model/all/', GetAllModelsByUser.as_view()),
    path('photo/locations/<location>/', AllPhotoByLocation.as_view()),
    path('photo/wells/<well>/', AllPhotoByWell.as_view()),
    path('test/', testDayModel),
    path('user/<int:user_id>/mask/<int:pk>/add/', addMask),
    path('user/<int:user_id>/mask/<int:pk>/remove/', removeMask),
    path('user/<int:user_id>/photo/<int:pk>/use-model/<int:model_id>', useUFmodel),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
