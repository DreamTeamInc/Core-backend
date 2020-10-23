from rest_framework import serializers
from .models import User, Photo


# class UserSerializer(serializers.ModelSerializer):
#   # user = serializers.HiddenField(default=serializers.CurrentUserDefault())
#   class Meta:
#     model = User
#     fields = "__all__"
class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password']


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class LocationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = '__all__'#['location']


class LocationDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = '__all__'


class WellListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ['well']


class WellDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = '__all__'
