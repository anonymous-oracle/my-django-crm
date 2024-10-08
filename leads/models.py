from django.db import models
# from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser

# Create your models here.
# User = get_user_model() # used to just demonstrate the built-in user class; do not user for serious use cases or applications

class User(AbstractUser):
    # cellphone_number = models.CharField(max_length=16)
    pass

class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # first_name = models.CharField(max_length=20) # already present in the user so not required
    # last_name = models.CharField(max_length=20)

class Lead(models.Model):
    SOURCE_CHOICES = [
        ('YouTube', 'YouTube'), 
        ('Google', 'Google'), 
        ('Newsletter', 'Newsletter'), 
    ]
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    age = models.IntegerField(default=0)
    agent = models.ForeignKey("Agent", on_delete=models.CASCADE)

    # agent = models.ForeignKey(Agent, on_delete=models.CASCADE) # if 'Agent' is without quotes then the Agent model should be defined before the model which has a foreign key reference to it 
    # phoned = models.BooleanField(default=False) # indicates whether a lead has been phoned; by default all leads are not phoned initially
    # source = models.CharField(choices=SOURCE_CHOICES, max_length=100)

    # profile_picture = models.ImageField(blank=True, null=True)
    # special_files = models.FileField(blank=True, null=True)