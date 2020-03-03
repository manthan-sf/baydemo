import jwt
import json
from uuid import uuid4

from django.shortcuts import HttpResponse
from django.shortcuts import get_object_or_404
from django.conf import settings as settings
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail, EmailMultiAlternatives
from django.contrib.auth import authenticate
from django.utils import timezone

from rest_framework import views, status, generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser

from .backends import JWTAuthentication
from .serializers import RegistrationSerializer, LoginSerializer, UserSerializer, ForgotPasswordSerializer
from .models import User, UserToken
from .renderers import UserJSONRenderer


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


class ForgotPassword(views.APIView):

    serializer_class = ForgotPasswordSerializer
    permission_classes = (AllowAny,)
    authentication_classes = []

    def post(self, request):
        email_object = request.data
        print(email_object, '11')

        try:
            user = get_object_or_404(User, email=email_object['email'])
        except:
            return Response({'email': "not valid"})
        token = str(uuid4())
        # user = validated_data.user
        data = {
            'user': user.id,
            'email': email_object['email'],
            'token': token
        }
        # print(data)
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            print(serializer.data)

            message = "http://127.0.0.1:8000/user/validate-token/%s/" % serializer.data['token']
            send_mail(
                subject='Subject here',
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=['manthananeja@gmail.com'],
                fail_silently=False,
            )
            return Response({"Email has been sent kindly check your inbox"}, status=200)
        else:
            print(serializer.errors)
            return Response(serializer.errors,  status=400)


class ValidateToken(views.APIView):

    permission_classes = (AllowAny,)
    authentication_classes = []

    def get(self, request, *args, **kwargs):
        token = kwargs['token']
        try:
            user_token = get_object_or_404(UserToken, token=token)
        except:
            return Response({"Invalid Token"}, status=403)
        if (timezone.now() - user_token.created).seconds > 600:
            return Response({'token expiration'}, status=403)
        else:
            return Response({"token validated"}, status=200)

# class SetPassword(views.APIView):

#     permission_classes = (AllowAny,)
#     authentication_classes = []

#     def post(self, request):
#         d
