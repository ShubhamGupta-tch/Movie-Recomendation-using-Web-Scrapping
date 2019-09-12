from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models

class CustomUserManager(UserManager):
    pass


class CustomUser(AbstractUser):
	objects = CustomUserManager()

class UserSearch(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    search = models.TextField()

    def __str__(self):
    	return self.user.username

    def save(self, **kwargs):
        super().save()
