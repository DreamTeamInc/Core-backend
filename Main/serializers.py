from rest_framework import serializers
from .models import User, Photo, Mask, Model


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password']


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class PhotoSerializer(serializers.ModelSerializer):
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


class MaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mask
        fields = '__all__'


class ModelSerializer(serializers.ModelSerializer):
    mask_set = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = Model
        exclude = ["model"]


class PhotoShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ["location", "well", "depth"]


class MaskDetailSerializer(serializers.ModelSerializer):
    photo = PhotoShortSerializer(many=False)
    class Meta:
        model = Mask
        fields = ["id", "user", "photo", "classification", "mask", "likes", "model", "users_who_like", "photo"]
