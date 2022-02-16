from rest_framework_simplejwt.serializers import serializers
from freelancer.models import Contract
from .models import *

class ClientSerializer(serializers.HyperlinkedModelSerializer):  
    class Meta:
        model = Client
        fields = ['sex', 'location', 'company', 'experience', 'photo']  

    def create(self, validated_data):
        user = self.context.get('user')
        sex = validated_data.get('sex')
        location = validated_data.get('location')
        company = validated_data.get('company')
        experience = validated_data.get('experience')
        photo = validated_data.get('photo', None)        
    
        client = Client(user=user, sex=sex, location=location, company=company, experience=experience, photo=photo)
        client.save()
        return client     

class JobSerializer(serializers.ModelSerializer):
    skill = serializers.ListField(child = serializers.CharField())  
    class Meta:
        model = Jobs        
        fields = ['title', 'description', 'duration', 'max_pay', 'skill']

    def create(self, validated_data):
        user = self.context.get('user')
        title = validated_data.get('title')
        description = validated_data.get('description')
        duration = validated_data.get('duration')
        max_pay = validated_data.get('max_pay')  
        skill_data = validated_data.get('skill')        
        client = Client.objects.get(user=user)
        
        job = Jobs(client=client, title=title, description=description, duration=duration, max_pay=max_pay)      
        job.save()        
        for skill in skill_data:
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

        