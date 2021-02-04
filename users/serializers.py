from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Profile
        # fields = (
        #     'id', 'description', 'phone_number', 'birth_date', 'avatar', 'role'
        # )
        read_only_fields = ('created_at', 'updated_at', 'role')        
        exclude = ('user',)
     
class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(required=False)
    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'first_name', 'last_name', 'profile'
        )