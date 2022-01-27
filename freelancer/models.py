from distutils.command.upload import upload
from django.db import models
from auth_app.models import User
from client.models import Jobs

# Create your models here.

class Freelancer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False, blank=False)  
    tag = models.CharField(max_length=30, blank=True, null=True)  
    sex = models.CharField(max_length = 6, blank=False, null=False)
    dob = models.DateField(blank= False, null=False)
    location = models.CharField(max_length = 30, null = False, blank = False)
    qualification = models.CharField(max_length=60, blank=True, null=True)
    experience = models.FloatField(blank=True, null=True)    
    photo = models.ImageField(upload_to='freelancerimg', blank=True, null=True)
    contribution = models.IntegerField(null=True, blank=True)
    is_verified = models.BooleanField(default = False)
    ratings = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.user.email

class Skills(models.Model):
    freelancer = models.ForeignKey(Freelancer, on_delete=models.CASCADE, null=False, blank=False)
    skill = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.skill

class Favourites(models.Model):
    freelancer = models.ForeignKey(Freelancer, on_delete=models.CASCADE, null=False, blank=False)
    job = models.ForeignKey(Jobs, on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self):
        return self.job.title

class Bids(models.Model):
    job = models.ForeignKey(Jobs, on_delete=models.CASCADE, null=False, blank=False)
    freelancer = models.ForeignKey(Freelancer, on_delete=models.CASCADE, null=False, blank=False)
    amount = models.IntegerField(null=False, blank=False)
    about = models.CharField(max_length=30, blank=True, null=True)
    bid_date = models.DateTimeField(auto_now_add=True,null=False, blank=False)

    def __str__(self):
        return self.job.title

class Contract(models.Model):
    job = models.OneToOneField(Jobs, on_delete=models.CASCADE, null=False, blank=False)
    freelancer = models.ForeignKey(Freelancer, on_delete=models.CASCADE, null=False, blank=False)
    start_date = models.DateTimeField(null= True, blank=True)
    end_date = models.DateTimeField(null= True, blank=True)
    subbmitted = models.BooleanField(default= False)
    review = models.CharField(max_length= 100, null=True, blank=True)