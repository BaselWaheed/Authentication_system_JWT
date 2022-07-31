from django.urls import path 
from . import views 
from rest_framework_simplejwt.views import TokenRefreshView




urlpatterns = [


    path('auth/SignUp/',views.RegistrationView.as_view(), name = 'SignUp'),

    path('auth/email-verify/',views.VerifyEmail.as_view(), name = 'verify'),

    path('auth/login/',views.LoginAPIView.as_view(), name = 'login'),

    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),



]
