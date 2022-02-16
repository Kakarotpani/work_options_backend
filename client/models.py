from distutils.command.upload import upload
from hashlib import blake2b
from django.db import models
from auth_app.models import User

# Create your models here.

class Client(models.Model):
    user= models.OneToOneField(User, on_delete=models.CASCADE, null=False, blank=False)
    sex = models.CharField(max_length = 6, blank=False, null=False)
    location = models.CharField(max_length = 30, null = False, blank = False)    
    company = models.CharField(max_length= 30, null= True, blank=True)
    experience = models.FloatField(blank=True, null=True)
    photo = models.ImageField(upload_to= 'clientimg', blank= True, null= True)
    contribution = models.IntegerField(null=True, blank=True, default=0)
    is_verified = models.BooleanField(default = False)

    def __str__(self):
        return self.user.email
    
class Jobs(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)    
    title = models.CharField(max_length= 60, blank=False, null=False)
    description = models.TextField(max_length= 120, blank=False, null=False)
    duration = models.IntegerField(blank= True, null=True)
    max_pay = models.FloatField(blank= False, null=False)
    post_date = models.DateField(auto_now_add=True, null=False, blank=False)
    is_finished = models.BooleanField(default=False)    
    
    def __str__(self):
        return self.title    
    
class Job_skills(models.Model):
    job = models.ForeignKey(Jobs, on_delete= models.CASCADE)
    skill = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.skill
