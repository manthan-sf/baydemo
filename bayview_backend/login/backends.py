import jwt
from django.conf import settings
from rest_framework import authentication, exceptions
from .models import User
from django.core.exceptions import PermissionDenied


class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):

        request.user = None

        auth_header = authentication.get_authorization_header(request)
        token = auth_header.decode('utf-8')
        print(token, '2222222')

        return self._authenticate_credentials(request, token)

    def _authenticate_credentials(self, request, token):
        """
        Try to authenticate the given credentials. If authentication is
        successful, return the user and token. If not, throw an error.
        """

        payload = {}

        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
            print('token ->', token, 'payload ->', payload)
        except:
            msg = 'Invalid Authentication, Could not decode token'
            raise exceptions.AuthenticationFailed(msg)

        try:
            user = User.objects.get(pk=payload['id'])
        except User.DoesNotExist:
            msg = 'No user matching this token was found.'
            raise exceptions.AuthenticationFailed(msg)

        if not user.is_active:
            msg = 'This user has been deactivated.'
            raise exceptions.AuthenticationFailed(msg)

        if request.path == '/user/':
            if user.is_staff:
                print('true')
            else:
                raise PermissionDenied()
        return (user, token)
