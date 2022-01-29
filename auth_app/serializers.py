from tkinter import NO
from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import update_last_login


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required = True, style = {'input_type' : 'password'})   
    password2 = serializers.CharField(required = True, write_only = True, style = {'input_type' : 'password'}) 
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'password', 'password2', 'is_freelancer', 'is_client']

    def create(self, validated_data):
        first_name = validated_data.get('first_name')
        last_name = validated_data.get('last_name')
        email = validated_data.get('email')
        phone = validated_data.get('phone')
        password = validated_data.get('password')
        password2 = validated_data.get('password2')
        is_freelancer = validated_data.get('is_freelancer')
        is_client = validated_data.get('is_client')

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'error': 'Email exits !!'})  

        if first_name.isdigit() or last_name.isdigit():
            raise serializers.ValidationError({'error': 'name in digit'})        
        
        if password == password2:    
            if is_freelancer == True:
                user = User(first_name = first_name, last_name= last_name, email= email, phone= phone, is_freelancer = True)
                user.set_password(password)
                user.save()
                return user

            elif is_client == True:
                user = User(first_name = first_name, last_name= last_name, email= email, phone= phone, is_client = True)
                user.set_password(password)
                user.save()
                return user 
        else:
            raise serializers.ValidationError({'error': 'password mismatch !!'})

        return super(UserSerializer,self).create(validated_data)

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(required= True, style = {'input_type' : 'password'})    

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")
        user = authenticate(email=email, password=password)
        if user:
            if user.is_active:
                update_last_login(None, user)
                return user               
            else:
                raise serializers.ValidationError({'error': 'user doesn\'t exist !!'})
        else:
            raise serializers.ValidationError({'error': 'INVALID credentials !!'})

