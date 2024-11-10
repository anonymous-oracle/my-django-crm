from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    is_organiser = models.BooleanField(default=True)
    is_agent = models.BooleanField(default=False) # if agent is assigned then the account is not an organiser account and will not have a userprofile

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self) -> str:
        return self.user.username
    
class Lead(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    age = models.IntegerField(default=0)
    organisation = models.ForeignKey(UserProfile, on_delete=models.CASCADE) # adding for the sake of filtering leads based on a particular organisation
    agent = models.ForeignKey("Agent", on_delete=models.SET_NULL, null=True, blank=True) # wrapping in quotes allows to define the Agent model class below the current class; else it would have had to be defined above the Lead class first
    category = models.ForeignKey("Category", on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name} | Assigned to: {self.agent}"

class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organisation = models.ForeignKey(UserProfile, on_delete=models.CASCADE) 

    def __str__(self) -> str:
        username = self.user.get_full_name() or self.user.get_short_name() or self.user.username
        return f"{username}"

class Category(models.Model):
    name = models.CharField(max_length=30) # new, contacted, converted, unconverted
    organisation = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name

    
def post_user_created_signal(sender, instance, created, **kwargs):
    if created: # executes further only if the instance is newly created
        UserProfile.objects.create(user=instance) # instance refers to the User object that was just created

# post save is a signal function used to trigger a signal whenever an object is created/saved by specifying the object model class in the sender field
post_save.connect(post_user_created_signal, sender=User) # the signal is sent whenever a user model is created