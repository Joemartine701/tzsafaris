from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from django.db.models import Q
class EmailAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        
        # Check if the username is an email or a phone number
        if '@' in username:
            user = UserModel.objects.filter(Q(email__iexact=username)).first()
        else:
            user = UserModel.objects.filter(Q(phone=username)).first()

        if user and user.check_password(password):
            return user
    # def authenticate(self, request, email=None, password=None):
    #     UserModel = get_user_model()
    #     try:
    #         user = UserModel.objects.get(email=email)
    #         if user.check_password(password):
    #             return user
    #     except UserModel.DoesNotExist:
    #         return None