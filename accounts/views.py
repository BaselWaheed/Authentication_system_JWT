from django.conf import settings
from accounts.models import User
from . import serializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.permissions import AllowAny, IsAuthenticated
from .utils import Util
import jwt
from django.contrib.auth import login as LOGIN
from rest_framework.renderers import TemplateHTMLRenderer

# Register For User

class RegistrationView(generics.GenericAPIView):  
    authentication_classes = ()
    permission_classes = (AllowAny,)
    serializer_class =serializer.RegisterSerializer
    def post(self , request ):
        serializer = self.get_serializer(data =request.data)
        serializer.is_valid(raise_exception= True)
        serializer.save()
        return Response({ 'status' : True ,'message' :'Check Your Mail to verify account'},status=status.HTTP_200_OK)



#verify user by link activate
class VerifyEmail(APIView):
    serializer_class = serializer.EmailVerificationSerializer
    renderer_classes = [TemplateHTMLRenderer]
    token_param_config = openapi.Parameter('token',in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)
    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self , request , **kwargs):
        token = request.GET.get('token')
        try :
            payload = jwt.decode(token,settings.SECRET_KEY,algorithms=['HS256'])
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({ 'status' : True ,'message' :'Congratolations  Your Email is Activated'},template_name='accounts/success_verify.html',status=status.HTTP_200_OK)

        except jwt.ExpiredSignatureError as identifier:
            return Response({ 'status' : False ,'message' :'Activation Link Expired'} ,template_name='accounts/success_verify.html',status=status.HTTP_400_BAD_REQUEST)

        except jwt.DecodeError as identifier:
            return Response({ 'status' : False ,'message' :'Token invalid'} ,template_name='accounts/success_verify.html',status=status.HTTP_400_BAD_REQUEST)

        

class LoginAPIView(generics.GenericAPIView):
    serializer_class = serializer.LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        LOGIN(request,user)
        data = {
            "first_name" :user.first_name ,
            "last_name" : user.last_name , 
            "email" : user.email ,
            "country" : user.country ,
            "phoneNumber" : str(user.phoneNumber) ,
            "access" : user.get_tokens_for_user()['access'],
            "refresh" : user.get_tokens_for_user()['refresh'],

        }
        return Response({
            'status': True, "message": 'Login successfully' ,  "data":data
        }, status=status.HTTP_200_OK)








