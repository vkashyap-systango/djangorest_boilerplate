from django.contrib.auth import authenticate, get_user_model, login as auth_login
from django.db import transaction
from django.utils.translation import ugettext as _
from rest_framework import serializers
import datetime

from users.models import BaseUser

class BaseUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    def validate(self, data, *args, **kwargs):
        print(data)
        return super(BaseUserSerializer, self).validate(data, *args, **kwargs)

    @transaction.atomic()
    def create(self, validated_data):
        print(validated_data)
        email = validated_data['email']
        user = BaseUser.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.first_name = (validated_data['first_name'])
        user.last_name = (validated_data['last_name'])
        user.save()
        return user

    class Meta:
        model = BaseUser
        fields = ('first_name', 'last_name', 'email', 'id', 'password')



class LoginSerializer(serializers.Serializer):

    """
    Serializer class used to validate a email and password.
    'email' is identified by the custom UserModel.USERNAME_FIELD.
    Returns a JSON Web Token that can be used to authenticate later calls.
    """
    email = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    @property
    def object(self):
        return self.validated_data

    def validate(self, attrs, *args, **kwargs):
        print(attrs)
        credentials = attrs
        user = authenticate(**credentials)
        if user:
            if not user.is_active:
                msg = _('User account is disabled.')
                raise serializers.ValidationError({'error_msg': msg})
            return {
                'user': user
            }
        else:
            msg = _('Please enter valid credentials.')
            raise serializers.ValidationError({'error_msg': msg})


class PasswordResetSerializer(serializers.Serializer):

    email = serializers.CharField(write_only=True)

    @property
    def object(self):
        return self.validated_data

    def validate(self, data):
        
        email = data.get('email')
        users = BaseUser.objects.filter(email=email)
        if users.count() != 0:
            return {'user':users[0]}
        else:
            msg = _('Email does not exist')
            raise serializers.ValidationError({'error_msg': msg})


    class Meta:
        model = BaseUser
        fields = ('email',)


class ConfirmPasswordResetSerializer(serializers.Serializer):

    u_id = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)