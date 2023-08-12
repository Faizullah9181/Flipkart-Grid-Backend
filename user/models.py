from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class UserAccountManager(BaseUserManager):
    def create_user(self, username, email, password=None):

        email = self.normalize_email(email)
        user = self.model(username=username, email=email)


        if not email:
            raise ValueError('User must have an email address')

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, email, password):
        user = self.create_user(username, email, password)

        user.is_superuser = True
        user.is_staff = True
        user.is_admin = True
        user.save(using=self._db)

        return user


class Users(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=100, unique=True,null=False, blank=False)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(max_length=255, unique=True)
    mobile_no = models.CharField(max_length=15, blank=True)
    image = models.CharField(max_length=255, blank=True)
    address = models.CharField(max_length=500, blank=True)
    gender =models.CharField(max_length=10,blank=True,default='Male')
    dob = models.DateField(null=True, blank=False)
    last_modified = models.DateTimeField(auto_now_add=True)
    is_profile_complete = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserAccountManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def get_full_name(self):
        return self.first_name

    def get_short_name(self):
        return self.first_name
    
    def __str__(self):
        return self.email