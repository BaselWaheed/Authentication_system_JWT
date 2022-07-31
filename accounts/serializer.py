from rest_framework import serializers
from django.contrib.sites.shortcuts import get_current_site
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .utils import Util
from .models import User
from django.urls import reverse



class RegisterSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required= True)
    last_name = serializers.CharField(required= True)
    email = serializers.EmailField(required= True)
    country = serializers.CharField(required= True)



    class Meta:
        model = User
        fields = ['id','first_name','last_name', 'email', 'password' ,'phoneNumber','country']
        read_only_fields = ['id']
        extra_kwargs={
            'password' :{'write_only':True}
        }
    
    def validate(self, attrs):
        email = attrs['email']
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'status' : False ,'message' :('email already exist')})
        if User.objects.filter(phoneNumber=attrs['phoneNumber']).exists():
            raise serializers.ValidationError({'status' : False ,'message' :('phone number already exist')})
        return attrs

    def save(self , **kwargs):
        user = User(
            first_name =self.validated_data['first_name'],
            last_name =self.validated_data['last_name'],
            email =self.validated_data['email'],
            phoneNumber= self.validated_data['phoneNumber'],
            country= self.validated_data['country'],
        )
        user.set_password(self.validated_data['password'])
        user.save()
        request = self.context['request']
        site = get_current_site(request).domain
        relativeLink = reverse('verify')
        token = RefreshToken.for_user(user).access_token
        link = 'http://'+site+relativeLink+"?token="+str(token)
        body = 'Click Following Link to verify Email\n'+ link
        data = {
            'title':'Email verification',
            'content':'basel waheed byt3lm ya nas' ,
            'body':body, 
            'to_email': user.email
        }
        Util.send_email(data)
        return user 
        


class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ['token']


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        filtered_user_by_email = User.objects.filter(email=email)
        user = authenticate(email=email, password=password)

        if filtered_user_by_email.exists() and filtered_user_by_email[0].auth_provider != 'email':
            raise serializers.AuthenticationFailed({"status":False,"message":'Please continue your login using'+ filtered_user_by_email[0].auth_provider})
        if not user:
            raise serializers.AuthenticationFailed({"status":False,"message":'Invalid credentials, try again'})
        if not user.is_active:
            raise serializers.AuthenticationFailed({"status":False,"message":'Account disabled, contact admin'})
        if not user.is_verified:
            raise serializers.AuthenticationFailed({"status":False,"message":'Email is not verified'})
        attrs['user'] = user
        return attrs

    

   
