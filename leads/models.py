from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    pass

class Lead(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    age = models.IntegerField(default=0)
    agent = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"Lead: {self.first_name} {self.last_name} | Assigned to: {self.agent}"

class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        username = self.user.get_full_name() or self.user.get_short_name() or self.user.username
        return f"Agent: {username}"