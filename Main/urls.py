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
    path('user/<int:user_id>/mask/<int:pk>/add/', addMask),
    path('user/<int:user_id>/mask/<int:pk>/remove/', removeMask),
    path('user/<int:user_id>/photo/<int:photo_id>/use_day_model/<int:model_id>/', use_daylight_model),
    path('user/<int:user_id>/photo/<int:photo_id>/use_uf_model/<int:model_id>/', use_UF_model),
    path('send_mask/', create_mask_daylight),
    path('user/<int:user_id>/get_active_model/', get_active_model),
    path('user/<int:user_id>/active_model/masks', all_masks_from_active_model),
    path('user/<int:user_id>/delete_active_model_masks/', del_all_masks_from_active_model),
    path('user/<int:user_id>/create_non_default_UF_model/<name>', create_non_default_UF_model),
    path('user/<int:user_id>/retrain_default_UF_model/', retrain_default_UF_model),
    path('user/<int:user_id>/photo/<int:photo_id>/get_mask_from_daylight_model/<int:model_id>/', get_mask_from_daylight_model),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
