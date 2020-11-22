import json
import numpy as np
from PIL import Image
from skimage import io
import io as IO
from matplotlib import pyplot as plt
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import User, Photo, Mask, Model
from .serializers import *
from .DataSienceUV.UV_Model import UV_Model
from App.settings import BASE_DIR
from .DataSienceDaylight import googleDrive


class CreateUser(generics.CreateAPIView):
    serializer_class = UserDetailSerializer


class GetAllUsers(generics.ListAPIView):
    serializer_class = UserListSerializer
    queryset = User.objects.all()


class PutGetDeleteOneUser(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserDetailSerializer
    queryset = User.objects.all()


class GetAllLocations(generics.ListAPIView):
    serializer_class =  PhotoSerializer
    queryset = Photo.objects.all()
    def get(self, request):
        locations = Photo.objects.all()
        if len(locations) == 0:
            return Response({"error": "no locations yet"})
        serializer =  PhotoSerializer(locations, many=True)
        res = []
        for location in serializer.data:
            res.append(location["location"])
        return Response({"locations": set(res)})


class CreatePhoto(generics.CreateAPIView):
    serializer_class =  PhotoSerializer
    def post(self, request):
        photo = ''
        if "photo" in request.FILES:
            photo = request.FILES['photo']
        else:
            return Response(data={"error":"no photo field or no file in request"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = PhotoSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        byte_photo = photo.read() # if too big image use this: for chunk in photo.chunks():   ...
        user = get_object_or_404(User, id=request.data["user"])
        Photo.objects.create(photo=byte_photo,
                             well=request.data["well"],
                             depth=request.data["depth"],
                             kind=request.data["kind"],
                             location=request.data["location"],
                             user=user)
        return Response({"response": "photo was successfully created"})


class GetAllPhotos(generics.ListAPIView):
    serializer_class = PhotoSerializer
    filterset_fields = ['kind', 'location', 'well']

    def get_queryset(self):
        queryset = Photo.objects.all()
        tagged = self.request.query_params.get('tagged', None)
        user_id = 0
        if 'token' in self.request.COOKIES and  self.request.COOKIES['token'] != 'None':
            user_id = self.request.COOKIES['token']
        # else:
        #     raise ValueError("No token")
        if tagged is not None:
            if tagged == "Размеченные":
                queryset = queryset.filter(mask__isnull=False).distinct()
            elif tagged == "Неразмеченные":
                queryset = queryset.filter(mask__isnull=True)
            elif tagged == "Размеченные мной":
                queryset = queryset.filter(mask__user=user_id).distinct()
            elif tagged == "Неразмеченные мной":
                queryset = queryset.filter(~Q(mask__user=user_id))
        return queryset
    # def get(self, request):
    #     try:
    #         queryset = self.get_queryset()
    #     except ValueError as e:
    #         return Response(data={"error:":"no token"}, status=status.HTTP_401_UNAUTHORIZED)
    #     serializer = self.serializer_class(queryset, many=True)
    #     return Response(data=serializer.data, status=status.HTTP_200_OK)


class PutGetDeleteOnePhoto(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PhotoSerializer
    queryset = Photo.objects.all()


@api_view(['POST'])
def create_mask_daylight(request):
    mask = ''
    if "mask" in request.FILES:
        mask = request.FILES['mask']
    else:
        return Response(data={"error":"no mask parameter or no file in request"}, status=status.HTTP_400_BAD_REQUEST)
    byte_mask = mask.read() # if too big image use this: for chunk in photo.chunks():   ...
    classification = {
        "0" : "Аргиллит",
        "1" : "Алевролит глинистый",
        "2" : "Песчаник",
        "3" : "Другое"
    }
    try:
        googleDrive.delete(mask.name.replace("mask", "photo"))
    except:
        pass
    photo_id, user_id, model_id = mask.name[4:-4].split('_')
    user = get_object_or_404(User, id=user_id)
    photo = get_object_or_404(Photo, id=photo_id)
    model = get_object_or_404(Model, id=model_id)
    mask = Mask.objects.create(user=user, photo=photo, classification=classification, mask=byte_mask)
    mask.model.add(model)
    return Response(data={"message":"mask {0} is successfully sent".format(mask.id)}, status=status.HTTP_200_OK)


@api_view(['GET'])
def use_daylight_model(request, photo_id, model_id):
    user_id = 0
    if 'token' in request.COOKIES and  request.COOKIES['token'] != 'None':
        user_id = request.COOKIES['token']
    else:
        return Response(data={"error":"no token"}, status=status.HTTP_401_UNAUTHORIZED)
    user = User.objects.get(id=user_id)
    model = Model.objects.filter(id=model_id)
    if model.count() == 0:
        return Response(data={"error":"no model with id {0}".format(model_id)}, status=status.HTTP_400_BAD_REQUEST)
    model = model[0]
    photo = Photo.objects.filter(id=photo_id)
    if photo.count() == 0:
        return Response(data={"error":"no photo with id {0}".format(photo_id)}, status=status.HTTP_400_BAD_REQUEST)
    photo = photo[0]
    if model.kind != photo.kind:
        return Response({"error":"no model {0} has {1} kind, while photo {2} - {3}".format(model.id, model.kind, photo.id, photo.kind)})
    with open("photo{0}_{1}_{2}.png".format(photo.id, user_id, model_id), 'wb') as imagefile:
        imagefile.write(photo.photo)
        googleDrive.upload(imagefile.name, "photo_predict")
    return Response(data={"message":"photo is getting segmented right now. Please wait a little."}, status=status.HTTP_200_OK)


@api_view(['GET'])
def use_UF_model(request, photo_id, model_id):
    user_id = 0
    if 'token' in request.COOKIES and  request.COOKIES['token'] != 'None':
        user_id = request.COOKIES['token']
    else:
        return Response(data={"error":"no token"}, status=status.HTTP_401_UNAUTHORIZED)
    user = User.objects.get(id=user_id)
    model = Model.objects.filter(id=model_id)
    if model.count() == 0:
        return Response(data={"error":"no model with id {0}".format(model_id)}, status=status.HTTP_400_BAD_REQUEST)
    model = model[0]
    photo = Photo.objects.filter(id=photo_id)
    if photo.count() == 0:
        return Response(data={"error":"no photo with id {0}".format(photo_id)}, status=status.HTTP_400_BAD_REQUEST)
    photo = photo[0]
    if model.kind != photo.kind:
        return Response({"error":"no model {0} has {1} kind, while photo {2} - {3}".format(model.id, model.kind, photo.id, photo.kind)})
    with open("photo{0}.png".format(photo.id), 'wb') as imagefile:
        imagefile.write(photo.photo)
        uv = 0
        if model.model:
            print("trained model")
            with open(model.model, 'rb') as modelfile:
                uv = UV_Model(model=modelfile)
        else:
            print("empty model")
            uv = UV_Model()
        
        f = io.imread(imagefile.name)
    mask = uv.predict(f)
    classification = { 
        "100" : "Отсутствует",
        "200" : "Насыщенное",
        "300" : "Карбонатное"
    }
        # mask_rgb = np.zeros([mask.shape[0], mask.shape[1],3], dtype=np.uint8)
        # mask_rgb[:,:,0] = mask
        # mask_rgb[:,:,1] = mask
        # mask_rgb[:,:,2] = mask
        # im = Image.fromarray(mask_rgb, 'RGB')
    im = Image.fromarray(mask)
    # im.show()
    im.save("mask{0}.png".format(photo.id))
        # a = np.asarray(im)
        # b = IO.BytesIO()
        # im.save(b, 'png')
        # im_bytes = b.getvalue()
    im_bytes = bytes()
    with open("mask{0}.png".format(photo.id), 'rb') as f:
        im_bytes = f.read()
    mask = Mask.objects.create(user=user, photo=photo, classification=classification, mask=im_bytes)
    mask.model.add(model)   
    serializer = MaskSerializer(mask)
    return Response(data=serializer.data, status=status.HTTP_200_OK)

    # return Response("Good")


@api_view(['PUT'])
def retrain_UF_model(request, model_id):
    # user_id = 0
    # if 'token' in request.COOKIES and  request.COOKIES['token'] != 'None':
    #     user_id = request.COOKIES['token']
    # else:
    #     return Response(data={"error":"no token"}, status=status.HTTP_401_UNAUTHORIZED)
    # user = User.objects.get(id=user_id)
    model = Model.objects.filter(id=model_id)
    if model.count() == 0:
        return Response(data={"error":"no model with id {0}".format(model_id)}, status=status.HTTP_400_BAD_REQUEST)
    model = model[0]
    if model.kind != 2:
        return Response(data={"error":"model {0} is not ultraviolet".format(model_id)}, status=status.HTTP_400_BAD_REQUEST)

    uv = 0
    if model.model:
        print("trained model")
        with open(model.model, 'rb') as modelfile:
            uv = UV_Model(model=modelfile)
    else:
        print("empty model")
        uv = UV_Model()

    mask_ids = request.POST.getlist('masks')
    masks = []
    photos = []
    jsons = []
    for mask_id in mask_ids:

        mask = get_object_or_404(Mask, id=mask_id)
        with open("mask{0}.png".format(mask_id), 'wb') as maskfile:
            maskfile.write(mask.mask)
        # was an error: could not find a format to read the specified file in single-image mode
        with open("mask{0}.png".format(mask_id), 'rb') as maskreadfile:
            masks.append(io.imread(maskreadfile.name, as_gray=True))
        
        photo = get_object_or_404(Photo, id=mask.photo.id)
        with open("photo{0}.png".format(photo.id), 'wb') as photofile:
            photofile.write(photo.photo)
            photos.append(io.imread(photofile.name))

        classification = mask.classification.replace("'", '"')
        jsons.append(json.loads(classification))

    print("hey2")
    uv.retrain(photos, masks, jsons)
    print("hey3")
    new_model = uv.save_model(model.name)
    print("len", len(new_model[0]))
    # with open(new_model[0], 'rb') as f:
    #     byte_model = f.read()
    # model.model = byte_model
    # model.save()
    return Response("Good")


class AllWells(generics.ListAPIView):
    serializer_class = WellListSerializer
    queryset = Photo.objects.all()
    def get(self, request):
        wells = Photo.objects.all()
        if len(wells) == 0:
            return Response({"error": "no wells yet"})
        serializer = WellListSerializer(wells, many=True)
        res = []
        for well in serializer.data:
            res.append(well["well"])
        return Response({"wells": set(res)})


class WellInLocation(generics.ListAPIView):
    serializer_class = WellDetailSerializer
    queryset = Photo.objects.all()
    def get(self, request, location):
        wells = Photo.objects.filter(location=location)
        if len(wells) == 0:
            return Response({"error": "no such wells in {0} location".format(location)})
        serializer = WellDetailSerializer(wells, many=True)
        res = []
        for well in serializer.data:
            res.append(well["well"])
        return Response({"well": set(res)})


class CreateMask(generics.CreateAPIView):
    serializer_class = MaskSerializer
    def post(self, request):
        mask = ''
        if 'mask' in request.FILES:
            mask = request.FILES['mask']
        else:
            return Response(data={"error":"no mask field or no file in request"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        byte_mask = mask.read()
        user = get_object_or_404(User, id=request.data["user"])
        photo = get_object_or_404(Photo, id=request.data["photo"])
        Mask.objects.create(mask=byte_mask,
                            classification=request.data["classification"],
                            user=user,
                            photo=photo)
        return Response({"response": "mask was successfully created"})


class GetAllMasks(generics.ListAPIView):
    serializer_class = MaskSerializer
    queryset = Mask.objects.all()


class PutGetDeleteOneMask(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MaskSerializer
    queryset = Mask.objects.all()


class CreateModel(generics.CreateAPIView):
    serializer_class = ModelSerializer


class GetAllModels(generics.ListAPIView):
    serializer_class = ModelSerializer
    queryset = Model.objects.all()


class GetAllModelsByUser(generics.ListAPIView):
    serializer_class = ModelSerializer
    queryset = Model.objects.all()
    def get(self, request, pk):
        user = User.objects.filter(id = pk)
        if len(user) == 0:
            return Response({"error": "there is no user with id {0}".format(pk)})
        models = Model.objects.filter(Q(user=pk) | Q(is_default=True))
        if len(models) == 0:
            return Response({"error": "user with id {0} has no models".format(pk)})
        serializer = ModelSerializer(models, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class PutGetDeleteOneModel(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ModelSerializer
    queryset = Model.objects.all()


class AllMaskByPhoto(generics.ListAPIView):
    serializer_class = MaskSerializer
    queryset = Mask.objects.all()
    def get(self, request, pk):
        photos = Photo.objects.filter(id = pk)
        if len(photos) == 0:
            return Response({"error": "there is no photo with id {0}".format(pk)})
        masks = Mask.objects.filter(photo=pk)
        if len(masks) == 0:
            return Response({"error": "photo with id {0} has no masks".format(pk)})
        serializer = MaskSerializer(masks, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class AllPhotoByLocation(generics.ListAPIView):
    serializer_class = PhotoSerializer
    def get_queryset(self):
        location = self.kwargs['location']
        return Photo.objects.filter(location=location)


class AllPhotoByWell(generics.ListAPIView):
    serializer_class = PhotoSerializer
    def get_queryset(self):
        well = self.kwargs['well']
        return Photo.objects.filter(well=well)


@api_view(['PUT'])
def addMask(request, user_id, pk): 
    user = User.objects.filter(id=user_id)
    if user.count() == 0:
        return Response({"error":"no user with id {0}".format(user_id)})
    mask = Mask.objects.filter(id=pk)
    if mask.count() == 0:
        return Response({"error":"no mask with id {0}".format(pk)})
    kind = mask[0].photo.kind
    model = Model.objects.filter(is_active=True, user=user_id, kind=kind)
    if model.count() == 0:
        return Response({"error":"user {0} has no active models with kind {1}".format(user_id, kind)})
    if model.count() > 1:
        return Response({"error":"user {0} has more than one active models with kind {1}".format(user_id, kind)})
    model[0].mask_set.add(mask[0])
    serializer = ModelSerializer(model[0], many=False)
    return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(['PUT'])
def removeMask(request, user_id, pk): 
    user = User.objects.filter(id=user_id)
    if user.count() == 0:
        return Response({"error":"no user with id {0}".format(user_id)})
    mask = Mask.objects.filter(id=pk)
    if mask.count() == 0:
        return Response({"error":"no mask with id {0}".format(pk)})
    kind = mask[0].photo.kind
    model = Model.objects.filter(is_active=True, user=user_id, kind=kind)
    if model.count() == 0:
        return Response({"error":"user {0} has no active models with kind {1}".format(user_id, kind)})
    if model.count() > 1:
        return Response({"error":"user {0} has more than one active models with kind {1}".format(user_id, kind)})
    model[0].mask_set.remove(mask[0])
    serializer = ModelSerializer(model[0], many=False)
    return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_active_model(request, user_id): 
    models = Model.objects.filter(is_active=True, user=user_id)
    serializer = ModelSerializer(models, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def all_masks_from_active_model(request, user_id): 
    masks = Mask.objects.filter(model__user=user_id, model__is_active=True, model__kind=2)
    serializer = MaskSerializer(masks, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(['PUT'])
def like(request, user_id, pk, mask_id):
    user = User.objects.filter(id=user_id)
    if user.count() == 0:
        return Response({"error": "there is no user with id {0}".format(user_id)})
    photos = Photo.objects.filter(id = pk)
    if len(photos) == 0:
        return Response({"error": "there is no photo with id {0}".format(pk)})
    mask = Mask.objects.filter(photo=pk, id = mask_id).first()
    if mask == None:
        return Response({"error": "photo {0} has no mask with id {1}".format(pk, mask_id)})
    if user[0] in mask.users_who_like.all():
        return Response({"error":"user with id {0} has already liked this mask".format(user_id)})
    mask.users_who_like.add(user_id)
    mask.likes += 1
    mask.save()
    return Response({'likes': mask.likes})


@api_view(['PUT'])
def disike(request, user_id, pk, mask_id):
    user = User.objects.filter(id=user_id)
    if user.count() == 0:
        return Response({"error": "there is no user with id {0}".format(user_id)})
    photos = Photo.objects.filter(id = pk)
    if len(photos) == 0:
        return Response({"error": "there is no photo with id {0}".format(pk)})
    mask = Mask.objects.filter(photo=pk, id = mask_id).first()
    if mask == None:
        return Response({"error": "photo {0} has no mask with id {1}".format(pk, mask_id)})
    if mask.likes == 0:
        return Response({'error': 'mask already has 0 likes'})
    if user[0] not in mask.users_who_like.all():
        return Response({"error":"user with id {0} has already disliked this mask or hasn't liked it yet".format(user_id)})
    mask.users_who_like.remove(user_id)
    mask.likes -= 1
    mask.save()
    return Response({'likes': mask.likes})


@csrf_exempt
def authentication(request):
    if request.method == 'GET':
        if 'token' in request.COOKIES and  request.COOKIES['token'] != 'None':
            value = request.COOKIES['token']
            user = User.objects.filter(id=value)
            if len(user) == 0:
                return JsonResponse({'isAuthoriezed': False})
            result = {
                'isAuthorized': True,
                'id': user[0].id,
                'first_name': user[0].first_name,
                'second_name': user[0].second_name,
                'patronymic': user[0].patronymic,
                'birth_date': user[0].birth_date,
                'email': user[0].email,
                'company': user[0].company,
                'position': user[0].position,
                'sex':user[0].sex,
                'is_su': user[0].is_su,
                'created_date': user[0].created_date,
            }
            return JsonResponse(result)
        else:
            return JsonResponse({'isAuthorized': False})
    if request.method == 'POST':
        req=json.loads(request.body)
        email = req['email']
        password = req['password']
        isRemember = req['isRemember']
        user = User.objects.filter(email=email)
        if len(user) == 0:
            return JsonResponse({'isAuthoriezed': False, 'erorr': 'wrong_email'})
        if password != user[0].password:
            return JsonResponse({'isAuthoriezed': False, 'erorr': 'wrong_password'})
        result = {
                'isAuthorized': True,
                'id': user[0].id,
                'first_name': user[0].first_name,
                'second_name': user[0].second_name,
                'patronymic': user[0].patronymic,
                'birth_date': user[0].birth_date,
                'email': user[0].email,
                'company': user[0].company,
                'position': user[0].position,
                'sex':user[0].sex,
                'is_su': user[0].is_su,
                'created_date': user[0].created_date,
            }
        response = JsonResponse(result)
        max_age = 10*60*60 if not isRemember else 6*60*60*24*30
        response.set_cookie("token", user[0].id, max_age=max_age)
        return response
    if request.method == 'DELETE':
        response = JsonResponse({'isAuthoriezed': False, 'status': 'OK'})
        response.set_cookie("token", None)
        return response
