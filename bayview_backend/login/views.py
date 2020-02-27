from django.shortcuts import HttpResponse
from .serializers import RegistrationSerializer, LoginSerializer, UserSerializer
from .models import User
from .renderers import UserJSONRenderer

from rest_framework import views, status, generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
# from rest_framework_jwt.settings import api_settings

import jwt
import json
from django.shortcuts import get_object_or_404
from django.conf import settings as settings
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail, EmailMultiAlternatives
from django.contrib.auth import authenticate
from .backends import JWTAuthentication


class RegistrationAPIView(views.APIView):

    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer
    renderer_classes = (UserJSONRenderer,)
    authentication_classes = []

    def post(self, request):
        user = request.data.get('user', {})
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginAPIView(views.APIView):
    permission_classes = (AllowAny,)
    authentication_classes = []
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        print(dir(request))
        user = request.data.get('user', {})
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer
    authentication_classes = (JWTAuthentication,)

    def retrieve(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user)
        # print(request.user)
        # if not serializer.data['is_superuser']:
        #     raise PermissionDenied()

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):

        payload = request.data.get('user', {})
        serializer = self.serializer_class(
            request.user, data=payload, partial=True
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
