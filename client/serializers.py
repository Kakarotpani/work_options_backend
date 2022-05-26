from rest_framework_simplejwt.serializers import serializers
from freelancer.models import Contract
from .models import *
import ast

class ClientSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Client
        fields = ['sex', 'location', 'company', 'photo']  

    def create(self, validated_data):
        user = self.context.get('user')
        sex = validated_data.get('sex')
        location = validated_data.get('location')
        company = validated_data.get('company')
        photo = validated_data.get('photo', None)  
        client = Client(user=user, sex=sex, location=location, company=company, photo=photo)
        client.save()
        return client

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone']

    def create(self, validated_data):
        user= validated_data.get('user')
        first_name = validated_data.get('first_name')
        last_name = validated_data.get('last_name')
        email = validated_data.get('email')
        phone = validated_data.get('phone')
        user_obj = User(id=user.id, first_name = first_name, last_name= last_name, email= email, phone= phone, is_client = True)
        user_obj.save()
        return user_obj

class JobSerializer(serializers.ModelSerializer):
    #skill = serializers.ListField(child = serializers.CharField())  
    skill = serializers.CharField()
    class Meta:
        model = Jobs        
        fields = ['title', 'description', 'duration', 'max_pay', 'skill']

    def create(self, validated_data):
        user = self.context.get('user')
        title = validated_data.get('title')
        description = validated_data.get('description')
        duration = validated_data.get('duration')
        max_pay = validated_data.get('max_pay') 
        skills_get = validated_data.get('skill')
        skills = ast.literal_eval(skills_get)      
        client = Client.objects.get(user=user)
        
        job = Jobs(client=client, title=title, description=description, duration=duration, max_pay=max_pay)      
        job.save()
        for skill in skills:
            print("Skill -----", skill)
            Job_skills.objects.create(job=job, skill=skill)
        return job

class HistorySerializer(serializers.ModelSerializer):
    ratings = serializers.IntegerField()
    class Meta:
        model = Contract
        fields = ['ratings', 'review']

    def create(self, validated_data):
        ratings = validated_data.get('ratings')
        review = validated_data.get('review')
        id = self.context.get('id')    

        contract = Contract.objects.get(id=id)
        contract.submitted = True
        contract.review = review
        contract.save()

        freelancer = contract.freelancer
        freelancer.ratings = ratings
        freelancer.is_verified =True
        
        contribution = freelancer.contribution
        if not contribution: 
            freelancer.contribution = 1
        else:
            freelancer.contribution = contribution + 1        
        freelancer.save()

        client = contract.job.client
        client.is_verified = True
        contribution = client.contribution
        if not contribution: 
            client.contribution = 1
        else:
            client.contribution = contribution + 1
        client.save()

        job = contract.job
        job.is_finished = True
        job.save()
        return contract

        