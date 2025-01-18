from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import User

class LoginTrack(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='login_track')
    last_login = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - Last login: {self.last_login}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)

    def __str__(self):
        return self.user.username
