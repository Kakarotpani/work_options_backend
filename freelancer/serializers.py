from logging.config import valid_ident
from wsgiref import validate
from rest_framework_simplejwt.serializers import serializers
from .models import *
import ast # string to list 

class FreelancerSerializer(serializers.ModelSerializer): 
    """ skill = serializers.ListField(
        child = serializers.CharField()) """ 
    class Meta:
        model = Freelancer
        fields = ['tag', 'sex', 'dob', 'location', 'qualification', 'experience', 'photo']

    def create(self, validated_data):
        user = self._context.get('user')
        tag = validated_data.get('tag')
        sex = validated_data.get('sex')
        dob = validated_data.get('dob')
        location = validated_data.get('location')
        qualification= validated_data.get('qualification')
        experience = validated_data.get('experience')
        photo = validated_data.get('photo', None)      
        #skill_data = validated_data.get('skill')

        freelancer = Freelancer(user=user, tag=tag, sex=sex, dob=dob, location=location, qualification=qualification, experience=experience, photo=photo)
        freelancer.save()
        """ for skill in skill_data:
            Skills.objects.create(freelancer=freelancer, skill=skill) """
        return freelancer

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
        user_obj = User(id=user.id, first_name = first_name, last_name= last_name, email= email, phone= phone, is_freelancer = True)
        user_obj.save()
        return user_obj

class SkillAddSerializer(serializers.ModelSerializer):
    """ skill = serializers.ListField(
        child = serializers.CharField())  """
    skill = serializers.CharField()
    class Meta:
        model= Skills
        fields = ['skill']

    def create(self, validated_data):
        user = self.context.get('user')
        skills = validated_data.get('skill')
        result = ast.literal_eval(skills)
        freelancer = Freelancer.objects.get(user=user)
        for skill in result:
            print("SKILL ===========", skill)
            Skills.objects.create(freelancer=freelancer, skill=skill)
        return object

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model= Skills
        fields = ['skill']

    def create(self, validatesd_data):
        id = self.context.get('id')
        skill = validatesd_data.get('skill')
        object = Skills(id=id, skill=skill)
        object.save()
        return object 

class BidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bids
        fields = ['amount', 'about']

    def create(self, validated_data):
        job_id = self.context.get('id')
        user = self.context.get('user')
        amount = validated_data.get('amount')
        about = validated_data.get('about')
        job = Jobs.objects.get(id=job_id)
        freelancer = Freelancer.objects.get(user=user)
        
        bid = Bids(job= job, freelancer=freelancer, amount=amount, about=about)
        bid.save()
        return bid
