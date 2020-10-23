from django.http import HttpResponse
from django.http import JsonResponse
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
import json
from .models import User, Photo
from .serializers import *


class CreateVUser(generics.CreateAPIView):
    serializer_class = UserDetailSerializer


class GetAllUsers(generics.ListAPIView):
    serializer_class = UserListSerializer
    queryset = User.objects.all()
    

class PutGetDeleteOneUser(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserDetailSerializer
    queryset = User.objects.all()


class GetAllLocations(generics.ListAPIView):
    serializer_class = LocationListSerializer
    queryset = Photo.objects.all()
    def get(self, request):
       locations = Photo.objects.all()
       if len(locations) == 0:
           return Response({"error": "no locations yet"})
       serializer = LocationListSerializer(locations, many=True)
       res = []
       for location in serializer.data:
           res.append(location["location"])
       return Response({"locations": set(res)})


class CreatePhoto(generics.CreateAPIView):
    serializer_class = LocationDetailSerializer


class PutGetDeleteOnePhoto(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LocationDetailSerializer
    queryset = Photo.objects.all()


class AllWells(generics.ListAPIView):
    serializer_class = WellListSerializer
    queryset = Photo.objects.all()
    def get(self, request):
       wells = Photo.objects.all()
       if len(wells) == 0:
           return Response({"error": "no wells yet"})
       serializer =WellListSerializer(wells, many=True)
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
