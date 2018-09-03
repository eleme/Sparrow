from dal.models import *
import datetime
from django.contrib.auth.models import User


class AccountDao:
    @staticmethod
    def get_userProfile_with_id(id):
        userProfile = UserProfile.objects.get(user__id=id)
        return userProfile

    @staticmethod
    def get_user_with_id(id):
        try:
            user = User.objects.get(id=id)
            return user
        except:
            return None

    @staticmethod
    def get_users_with_username(username):
        users = list(User.objects.filter(username__contains=username).values('id',
                                                                             'username',
                                                                             'email'))
        return users

    @staticmethod
    def get_default_group():
        try:
            group = Group.objects.get(name='default_group')
            return group
        except:
            return None
