# serializers for the user api view
from django.contrib.auth import (get_user_model, authenticate)
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    # serializer for the user object

    class Meta:
        model = get_user_model()
        fields = ["email", "password", "name"]
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if (password):
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    # serializer for the user auth token
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        request = self.context.get('request')
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(request, username=email, password=password)

        if not user:
            raise serializers.ValidationError(
                'User Authentication failed', code='authorization')
        attrs['user'] = user
        print(attrs)
        return attrs
