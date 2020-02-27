from .models import User
from django.shortcuts import get_object_or_404
from .serializers import RegistrationSerializer

from rest_framework.response import Response


# class User_DB():
#     def get_all_Users(self):
#         users = User.objects.all()
#         return users

#     def get_user_by_username(username):
#         user = get_object_or_404(User, username=username)
#         return user

#     def get_user(username, password):
#         user = get_object_or_404(User, username=username, password=password)
#         return user

#     def update_user(payload, old_password):
#         user = get_object_or_404(
#             User, username=payload['username'], password=old_password)

#         # updated_user = {
#         #     "username": payload['username'],
#         #     "password": payload['password'],
#         #     "is_active": payload['is_active'],
#         #     "is_admin": payload['is_admin'],
#         #     "is_registered": payload['is_registered'],
#         #     "first_name": payload['first_name'],
#         #     "last_name": payload['last_name']
#         #     # "email": payload['email']
#         # }
#         serialized_user = UserSerializer(user, payload)

#         if serialized_user.is_valid():
#             serialized_user.save()
#             return {"result": True}
#         else:
#             return {"result": False, "errors": serialized_user.errors}
