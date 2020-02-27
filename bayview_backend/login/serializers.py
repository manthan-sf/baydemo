from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate


class RegistrationSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    # token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        # List all of the fields that could possibly be included in a request
        # or response, including fields specified explicitly above.
        fields = ['id', 'first_name', 'last_name',
                  'username', 'email', 'is_active', 'is_staff', 'password']

    def create(self, validated_data):
        # Use the `create_user` method we wrote earlier to create a new user.
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):

        username = data.get('username', None)
        password = data.get('password', None)

        if username is None:
            raise serializers.ValidationError("Username is required to login")

        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.')
        user = authenticate(username=username, password=password)
        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found.'
            )

        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )
        return {
            'username': user.username,
            'token': user.token
        }


class UserSerializer(serializers.ModelSerializer):
    """Handles serialization and deserialization of User objects."""

    # password = serializers.CharField(
    #     max_length=128,
    #     min_length=8,
    #     write_only=True
    # )

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name',
                  'last_name', 'is_active', 'is_staff']

    def update(self, instance, validated_data):
        """Performs an update on a User."""

        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance
