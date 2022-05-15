from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.conf import settings


class UserProfileManager(BaseUserManager):
    """Manager for user profiles"""

    def create_user(self, email, name, password=None):
        """Create a new user profile"""
        if not email:
            raise ValueError('User must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, name=name)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, password):
        """Create and save a new superuser with given details"""
        user = self.create_user(email, name, password)

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Database model for users in the system"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    favorites = models.TextField(default="") # {data_object_id, ...}
    voted = models.TextField(default="") # {data_object_id : 1/0/-1, ... }

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        """Retrieve full name of user"""
        return self.name

    def get_short_name(self):
        """Retrieve shot name of user"""
        return self.name

    def __str__(self):
        """Return string representation of our user"""
        return self.email


class SearchItem(models.Model):
    # id = models.IntegerField()
    createdAt = models.DateTimeField(auto_now_add=True)
    contentContributorId = models.CharField(max_length=255, default="sshm")
    contentContributorScore = models.IntegerField(default=0)
    contentTitle = models.CharField(max_length=500, default="")
    popularityName = models.CharField(max_length=255, default="")
    popularityValue = models.IntegerField(default=0)
    sourceName = models.CharField(max_length=255, default="")
    sourceOrder = models.IntegerField(default=0)
    sourceUrl = models.CharField(max_length=500, default="")
    vote = models.IntegerField(default=0)

    def __str__(self):
        """Return the model as a string"""
        return self.contentTitle


class ProfileFeedItem(models.Model):
    """Profile status update"""
    # user_profile = models.ForeignKey(
    #     settings.AUTH_USER_MODEL,
    #     on_delete=models.CASCADE
    # )
    createdAt = models.DateTimeField(auto_now_add=True)
    contentContributorId = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL, null=True
    )
    # contentContributorId = models.CharField(max_length=255)
    contentContributorScore = models.IntegerField(default=0)
    contentTitle = models.CharField(max_length=500, default="")
    sourceName = models.CharField(max_length=255, default="")
    sourceUrl = models.CharField(max_length=500, default="")
    vote = models.IntegerField(default=0)
    query = models.CharField(max_length=200, default="")

    def __str__(self):
        """Return the model as a string"""
        return self.contentTitle
