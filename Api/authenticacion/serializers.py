from rest_framework import serializers
from .models import CustomUser, Profile



class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['biography', 'phone', 'linkedin_profile', 'address']  # Incluye los campos que deseas



class UserSerializer(serializers.ModelSerializer):
    initials = serializers.SerializerMethodField()
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = CustomUser
        fields = '__all__'
        read_only_fields = ['id']

    def get_initials(self , obj):
         return obj.get_initials()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
            user = CustomUser(
                email=validated_data['email'],
                username=validated_data['username']
            )
            user.set_password(validated_data['password'])
            user.save()
            return user