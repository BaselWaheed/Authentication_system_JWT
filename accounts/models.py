from django.db import models
from django.contrib.auth.models import AbstractBaseUser , PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from .manager import CustomUserManager
from phonenumber_field.modelfields import PhoneNumberField
from rest_framework_simplejwt.tokens import RefreshToken

AUTH_PROVIDERS = {'facebook': 'facebook', 'google': 'google','twitter': 'twitter', 'email': 'email'}


class User(AbstractBaseUser,PermissionsMixin):

    first_name = models.CharField(_("firstname"), max_length=50)
    last_name = models.CharField(_("lastname"), max_length=50)
    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to='myphoto/%Y/%m/%d/', null=True,blank=True ,max_length=255)
    phoneNumber = PhoneNumberField(unique = True, null = True, blank = False)
    country = models.CharField(max_length=50 , null=True , blank=True)
    auth_provider = models.CharField(max_length=255, blank=False,null=False, default=AUTH_PROVIDERS.get('email'))

    objects = CustomUserManager()


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []



    def __str__(self):
        return self.email

    def get_tokens_for_user(user):
        refresh = RefreshToken.for_user(user)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }