from django.shortcuts import render

from accounts.models import User
from . import serializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import  IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework_simplejwt.authentication import JWTAuthentication
class UserProfileAPI(generics.RetrieveUpdateAPIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = serializer.UserSerializer


    def get_object(self):
        queryset = User.objects.get(email=self.request.user)
        return queryset

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({"status":True , "message":"Your Profile Is HERE" , "data": serializer.data},status=status.HTTP_200_OK)

    token_param_config = openapi.Parameter('token',in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)
    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request, *args, **kwargs):
        
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)






