
# serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from base.models import Profile, Product  # Assuming Profile is in base.models

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)

    class Meta:
        model = Profile
        fields = ('user', 'first_name', 'last_name', 'email')

# base/serializer.py
from rest_framework import serializers
from django.contrib.auth.models import User
from base.models import Profile  # Assuming Profile is in base.models

class UserRegistrationSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')

    def create(self, validated_data):
        # Check if the user already exists
        if User.objects.filter(username=validated_data['username']).exists():
            raise serializers.ValidationError({"username": "This username is already taken."})
        if User.objects.filter(email=validated_data['email']).exists():
            raise serializers.ValidationError({"email": "This email is already registered."})

        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])  # Hash the password
        user.save()

        # Create a profile if it does not already exist
        Profile.objects.get_or_create(user=user, defaults={
            'first_name': validated_data['first_name'],
            'last_name': validated_data['last_name'],
            'email': validated_data['email']
        })

        return user

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
