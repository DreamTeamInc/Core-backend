from rest_framework import serializers
from .models import User


# class UserSerializer(serializers.ModelSerializer):
#   # user = serializers.HiddenField(default=serializers.CurrentUserDefault())
#   class Meta:
#     model = User
#     fields = "__all__"
class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'second_name', "patronymic", "birth_date",
        "email","company", "position", "sex", "is_su", "created_date")


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
