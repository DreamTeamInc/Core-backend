from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
import json
# from skimage.segmentation import felzenszwalb
from .models import User
# from .serializers import UserSerializer
# from rest_framework.viewsets import ModelViewSet
from .serializers import *


def index(request):
    return HttpResponse("Hello World!")


@csrf_exempt
def loadphoto(request):
    if request.method == "POST":
        photo = request.FILES['file']
        # segments = felzenszwalb(photo, scale=50, sigma=10, min_size=100)  # return numpy.ndarray
        # lists = segments.tolist()
        # json_str = json.dumps(lists)
        return HttpResponse(photo, content_type = "multipart/form-data")
    else:
        return HttpResponse("<h2>No photo yet</h2>")


class UserCreateView(generics.CreateAPIView):
    serializer_class = UserDetailSerializer


class UserListView(generics.ListAPIView):
    serializer_class = UserListSerializer
    queryset = User.objects.all()


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserDetailSerializer
    queryset = User.objects.all()


@csrf_exempt
def authentication(request):
    if request.method == 'GET':
        if 'token' in request.COOKIES:
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
