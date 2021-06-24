
from django.contrib.auth import authenticate, get_user_model
from django.core import exceptions as django_exceptions
from django.contrib.auth.password_validation import validate_password
from django.db import IntegrityError, transaction

from djoser.conf import settings
from djoser.serializers import TokenCreateSerializer, UserCreateSerializer

from rest_framework import serializers

User = get_user_model()

class CustomTokenCreateSerializer(TokenCreateSerializer):

    def validate(self, attrs):
        password = attrs.get("password")
        params = {settings.LOGIN_FIELD: attrs.get(settings.LOGIN_FIELD)}
        self.user = authenticate(
            request=self.context.get("request"), **params, password=password # authenticate user
        )
        if not self.user:
            self.user = User.objects.filter(**params).first()
            if self.user and not self.user.check_password(password):
                self.fail("invalid_credentials")
        if self.user: # and self.user.is_active:
            return attrs
        self.fail("invalid_credentials")

class UserCreateSerializer(UserCreateSerializer):

    # method used to validate username, email and password
    def validate(self, attrs):
        user = User(**attrs)
        print(attrs)
        password = attrs.get("password")
        email = attrs.get("email")
        
        if User.objects.filter(email=email).exists(): # check if email already exist
            raise serializers.ValidationError("Email already exists")

        try:
            validate_password(password, user) # method that validates username and password
        except django_exceptions.ValidationError as e:
            serializer_error = serializers.as_serializer_error(e)
            raise serializers.ValidationError(
                {"password": serializer_error["non_field_errors"]}
            )
        return attrs

class UserSerializer(serializers.ModelSerializer):
    registration_timestamp = serializers.SerializerMethodField()
    activated = serializers.SerializerMethodField()

    def get_activated(self, sample):
        return sample.is_active

    def get_registration_timestamp(self, sample):
        return sample.date_joined
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'registration_timestamp', 'activated']
        ref_name = "User Serializer"