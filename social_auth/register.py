from django.contrib.auth import authenticate
from accounts.models import User
import os
import random
from rest_framework.exceptions import AuthenticationFailed


def generate_username(name):

    username = "".join(name.split(' ')).lower()
    if not User.objects.filter(username=username).exists():
        return username
    else:
        random_username = username + str(random.randint(0, 1000))
        return generate_username(random_username)


def register_social_user(provider, user_id, email, name):
    
    filtered_user_by_email = User.objects.filter(email=email)
  
    if filtered_user_by_email.exists():
        
        if provider == filtered_user_by_email[0].auth_provider:
            registered_user = authenticate(
                email=email, password=os.environ.get('SOCIAL_SECRET'))

            return {
                'first_name': registered_user.first_name,
                'last_name': registered_user.last_name,
                'email': registered_user.email,
                "country" : registered_user.country ,
                "phoneNumber" : str(registered_user.phoneNumber) ,
                "access" : registered_user.get_tokens_for_user()['access'],
                "refresh" : registered_user.get_tokens_for_user()['refresh'],
                
                }
        else:
            raise AuthenticationFailed(
                detail='Please continue your login using ' + filtered_user_by_email[0].auth_provider)

    else :
        newuser = User(
            email=email,
            first_name= name,
            id= user_id,
        )
        newuser.set_password(os.environ.get('SOCIAL_SECRET'))
        newuser.is_verified = True
        newuser.auth_provider = provider
        # new_user.phoneNumber = +20
        newuser.save()
        print("baselwaheed")
        new_user = authenticate(email=email, password=os.environ.get('SOCIAL_SECRET'))
        
        return {
            "first_name" :new_user.first_name ,
            "last_name" : new_user.last_name , 
            "email" : new_user.email ,
            "country" : new_user.country ,
            "phoneNumber" : str(new_user.phoneNumber),
            "access" : new_user.get_tokens_for_user()['access'],
            "refresh" : new_user.get_tokens_for_user()['refresh'],
        }
