from django.db import models

# Create your models here.
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)


class UserManager(BaseUserManager):
    #manager for users of the app.

    def create_user(self, email, password=None, **extra_fields):
        #Create, save, and return a new user
        if not email:
            raise ValueError('User must have an email adress') #error whe ther is no email provided by the user
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        #Craete, save and return a super user
        if not email:
            raise ValueError('User must have an email adress.')
        user = self.create_user(email, password)
        user.is_superuser= True
        user.is_staff = True
        user.save(using=self._db)

        return user



class User(AbstractBaseUser, PermissionsMixin):
    #user in the system
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = UserManager()
    USERNAME_FIELD = 'email'