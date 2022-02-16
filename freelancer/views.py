import itertools
from rest_framework.generics import GenericAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from auth_app.custom_permissions import IsClient, IsFreelancer
from .models import *
from client.models import *
from auth_app.models import User
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from django.db.models import Q
from django.shortcuts import get_object_or_404

class FreelancerProfile(GenericAPIView):
    permission_classes= [IsAuthenticated, IsFreelancer]
    
    # register freelancer
    def post(self, request):    
        user = request.user
        serializer = FreelancerSerializer(context= {'user':user}, data= request.data)
        if serializer.is_valid():      
            if user.is_freelancer: 
                serializer.save()           
                return Response({              
                    'data': 'updated profile Successfully !!',
                    'status' : status.HTTP_201_CREATED,
                })
        else:
            return Response(data= 'Invalid Form !!', status= status.HTTP_400_BAD_REQUEST)

    def get(self, request):     
        user = request.user
        try:  
            photo_url = "http://localhost:8000/media/"           
            freelancer = Freelancer.objects.get(user=user) 
            skills = Skills.objects.filter(freelancer=freelancer) 
            skill_list=[]
            for skills in skills: 
                skill_list = skill_list+ [{skills.id : skills.skill}]
            payload = {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'phone': str(user.phone),
            'tag': freelancer.tag,
            'sex': freelancer.sex,
            'dob': freelancer.dob,
            'location': freelancer.location,
            'qualification': freelancer.qualification,
            'experience': freelancer.experience,
            'photo': photo_url + str(freelancer.photo),
            'contribution': freelancer.contribution,
            'is_verified': freelancer.is_verified,
            'ratings': freelancer.ratings,
            'skill': skill_list }
            return Response(data= payload, status= status.HTTP_200_OK, content_type="application/json")
        except Exception as e:
            return Response(data= 'Couldn\'t fetch !!', status= status.HTTP_400_BAD_REQUEST)

    def put(self, request):     
        user= request.user
        freelancer= Freelancer.objects.get(user=user)
        serializer = FreelancerSerializer(instance=freelancer, data= request.data, context= {'user':user})
        if serializer.is_valid():    
            serializer.save()           
            return Response({              
                'data': 'updated profile Successfully !!',
                'status' : status.HTTP_201_CREATED })
        else:
            return Response({'data': 'Invalid Form !!', 'status': status.HTTP_400_BAD_REQUEST})

    def delete(self, request):      
        try:
            user= User.objects.get(user = request.user)            
            user.delete()
            return Response(data= 'Account Deleted ....', status= status.HTTP_200_OK)
        except Exception as e:
            return Response(data= 'Something Went Wrong !!', status= status.HTTP_400_BAD_REQUEST)   


class Skill(GenericAPIView):
    permission_classes = [IsAuthenticated, IsFreelancer]

    def post(self, request): 
        serializer = SkillSerializer(context={'user': request.user}, data=request.data)
        if serializer.save():
            serializer.save()
            return Response(data="skill added...", status=status.HTTP_200_OK)
        else:
            return Response(data="Couldn\'t add !!", status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
            
    def get(self, request):    
        freelancer = Freelancer.objects.get(user=request.user)
        skills = Skills.objects.filter(freelancer=freelancer)
        skill_list=[]
        if skills:
            for skills in skills: 
                skill_list = skill_list+ [{skills.id : skills.skill}]
            return Response(data=skill_list, statius=status.HTTP_200_OK)
        else:
            return Response(data="no skills yet", status=status.HTTP_200_OK)

    def put(self,request, id):    
        skill = Skills.objects.get(id=id)
        serializer = SkillSerializer(instance=skill, context={'id':id}, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(data="Couldn\'t update !!", status=status.HTTP_500_INTERNAL_SERVER_ERROR) 

    def delete(self,request, id):     
        try:
            skill = Skills.objects.get(id=id) 
            skill.delete()       
            return Response(data="skill deleted", status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data="Couldn\'t delete !!", status=status.HTTP_500_INTERNAL_SERVER_ERROR)     


class Bid(GenericAPIView):
    permission_classes = [IsAuthenticated, IsFreelancer]

    # add your bid
    def post(self, request, id): 
        job = Jobs.objects.get(id=id)
        if Contract.objects.filter(job=job).exists():
            return Response(data="NO more bid, contract given", status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            serializer = BidSerializer(context= {'user':request.user, 'id':id}, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(data="bid added successfully !!", status=status.HTTP_201_CREATED)
            else:
                return Response(data= 'Invalid Form !!', status= status.HTTP_400_BAD_REQUEST)

    # Applied jobs
    def get(self, request): 
        freelancer = Freelancer.objects.get(user= request.user)
        bids = Bids.objects.filter(freelancer=freelancer) 
        if bids:
            payload= []  
            for bid in bids:
                if not Contract.objects.filter(job=bid.job).exists():
                    payload = payload + [{
                        'job_id': bid.job.id,
                        'bids': Bids.objects.filter(job=bid.job).count(),
                        'title': bid.job.title,
                        'description': bid.job.description,
                        'duration': bid.job.duration,
                        'max_pay': bid.job.max_pay,
                        'post_date': bid.job.post_date,
                        'client': bid.job.client.user.first_name,
                        'email': bid.job.client.user.email,
                        'bid_id': bid.id,
                        'amount': bid.amount,
                        'about':  bid.about,
                        'bid_date': bid.bid_date }]
            return Response(data = payload, status= status.HTTP_200_OK)
        else:
            return Response({'data': 'No Bids yet....', 'status': status.HTTP_200_OK})

    # update bid data
    def put(self, request, id):
        bid = Bids.objects.get(id=id)
        serializer = BidSerializer(
            instance=bid, context= {'user':request.user, 'id':id}, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data="bid updated successfully !!", status=status.HTTP_201_CREATED)
        else:
            return Response(data= 'Couldn\'t update !!', status= status.HTTP_400_BAD_REQUEST)        

    def delete(self, request, id):
        try:
            bid = Bids.objects.get(id=id)
            bid.delete()
            return Response(data="bid deleted", status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data="Couldn\'t delete !!", status=status.HTTP_500_INTERNAL_SERVER_ERROR)  


class Favourite(GenericAPIView):
    permission_classes = [IsAuthenticated, IsFreelancer]

    def post(self, request, id):
        try:
            freelancer = Freelancer.objects.get(user=request.user)
            job = Jobs.objects.get(id=id)
            fav = Favourites(freelancer=freelancer, job=job)
            fav.save()
            return Response(data="added to favourite", status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data="Couldn\'t add!!", status=status.HTTP_500_INTERNAL_SERVER_ERROR)  

    def get(self, request):
        freelancer = Freelancer.objects.get(user=request.user)
        favs = Favourites.objects.filter(freelancer=freelancer)         
        if favs:        
            payload= []
            for fav in favs:
                if not Contract.objects.filter(job=fav.job).exists():       
                    skills = Job_skills.objects.filter(job= fav.job)  
                    skill_list = []   
                    for skill in skills:
                        skill_list = skill_list + [{skill.id: skill.skill}]  
                    payload = payload + [{
                        'job_id': fav.job.id,                        
                        'bids': Bids.objects.filter(job=fav.job).count(),
                        'title': fav.job.title,
                        'description': fav.job.description,
                        'duration': fav.job.duration,
                        'max_pay': fav.job.max_pay,
                        'post_date': fav.job.post_date,
                        'client': fav.job.client.user.first_name,
                        'email': fav.job.client.user.email,
                        'fav_id': fav.id,
                        'skill_list': skill_list,                        
                    }]
            return Response(data = payload, status= status.HTTP_200_OK)
        else:
            return Response({'data': 'No Favourites yet....', 'status': status.HTTP_200_OK})
    
    def delete(self, request, id):
        try:
            fav = Favourites.objects.get(id=id)
            fav.delete()
            return Response(data="removed from favourite", status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data="Couldn\'t remove from fav !!", status=status.HTTP_500_INTERNAL_SERVER_ERROR) 


class Contracts(GenericAPIView):
    permission_classes = [IsAuthenticated, IsFreelancer]

    # current jobs
    def get(self, request): 
        freelancer = Freelancer.objects.get(user= request.user)
        contracts = Contract.objects.filter(freelancer= freelancer)
        if contracts:
            payload= []
            for contract in contracts:
                if not contract.submitted:
                    bid = Bids.objects.filter(Q(job=contract.job) & Q(freelancer=freelancer)) 
                    for bid in bid:     
                        print(contract.job, bid.amount)        
                        payload = payload + [{
                            'job_id': contract.job.id,
                            'title': contract.job.title,
                            'description': contract.job.description,
                            'duration': contract.job.duration,
                            'max_pay': contract.job.max_pay,
                            'post_date': contract.job.post_date,
                            'client': contract.job.client.user.first_name,
                            'email': contract.job.client.user.email,
                            'phone': str(contract.job.client.user.phone),
                            'amount': bid.amount,
                            'start_date': contract.start_date,
                            'deadline':contract.end_date
                        }]
                    else:
                        pass
            return Response(data = payload, status= status.HTTP_200_OK)
        else:
            return Response(data= 'No Contracts yet', status= status.HTTP_200_OK)

        
class History(GenericAPIView):
    permission_classes=[IsAuthenticated, IsFreelancer]

    # finished job
    def get(self, request): 
        freelancer = Freelancer.objects.get(user=request.user)
        contracts = Contract.objects.filter(Q(freelancer=freelancer) & Q(submitted=True))         
        if contracts:
            payload = []
            for contract in contracts:
                bid = Bids.objects.get(Q(job=contract.job) & Q(freelancer=contract.freelancer))
                payload = payload + [{
                    'job_id': contract.job.id,
                    'title': contract.job.title,
                    'description': contract.job.description,
                    'post_date': contract.job.post_date,
                    'submit_date': contract.end_date,
                    'freelancer': contract.freelancer.user.first_name+" "+contract.freelancer.user.last_name,
                    'bid': bid.amount,
                    'review': contract.review,
                }]
            return Response(data= payload, status= status.HTTP_200_OK)
        else:
            return Response(data= 'no jobs to show in History', status= status.HTTP_200_OK)
        
class ClientProfile(GenericAPIView): 
    permission_classes = [IsFreelancer, IsFreelancer]

    def get(self, request, id):       
        try:            
            job= Jobs.objects.get(id=id)            
            client= job.client
            photo_url = "http://localhost:8000/media/"                    
            payload = {
                'id': client.user.id,
                'first_name': client.user.first_name,
                'last_name': client.user.last_name,
                'email': client.user.email,
                'phone': str(client.user.phone),
                'sex': client.sex,
                'location': client.location,
                'company': client.company,
                'experience': client.experience,
                'photo': photo_url + str(client.photo),
                'contribution': client.contribution,
                'is_verified': client.is_verified,            
            }
            return Response(data= payload, status= status.HTTP_200_OK, content_type="application/json")
        except Exception as e:
            return Response(data= 'Couldn\'t fetch !!', status= status.HTTP_400_BAD_REQUEST)


class Recommend(GenericAPIView):
    permission_classes = [IsAuthenticated, IsFreelancer]

    def get(self, request):
        freelancer = Freelancer.objects.get(user=request.user)
        skills = Skills.objects.filter(freelancer=freelancer)
        payload = []
        if skills:
            for skill in skills:                
                if Job_skills.objects.filter(skill=skill.skill).exists():
                    results = Job_skills.objects.filter(skill=skill.skill)                    
                    for result in results:
                        payload = payload + [{
                            'title':result.job.title,
                            'job_id':result.job.id,
                            'client':result.job.client.user.first_name+" "+result.job.client.user.last_name,
                            'max_pay':result.job.max_pay,
                            'duration':result.job.duration
                        }]
                else:
                    jobs= Jobs.objects.all()[:4]
                    job_list = []
                    for job in jobs:
                        job_list = job_list+[{
                            'title':job.title,
                            'job_id':job.id,
                            'client':job.client.user.first_name+" "+job.client.user.last_name,
                            'max_pay':job.max_pay,
                            'duration':job.duration
                        }]
                    return Response(data=job_list, status= status.HTTP_200_OK)
            return Response(data=payload, status=status.HTTP_200_OK)
        else:
            jobs= Jobs.objects.all()[:4]
            job_list = []
            for job in jobs:
                job_list = job_list+[{
                    'title':job.title,
                    'job_id':job.id,
                    'client':job.client.user.first_name+" "+job.client.user.last_name,
                    'max_pay':job.max_pay,
                    'duration':job.duration
                }]
            return Response(data=job_list, status= status.HTTP_200_OK)


class Search(GenericAPIView):
    permission_classes = [IsAuthenticated, IsFreelancer]
    
    def get(self, request):
        search = request.data.get('search')
        skill =  get_object_or_404(Job_skills, skill__icontains = search)
        if skill:
            payload = {
                'id': skill.id,
                'job': skill.job.title,
                'post_date': skill.job.post_date,
                'max_pay': skill.job.max_pay,
                'duration': skill.job.duration,
                'client': skill.job.client.user.first_name               
            }
            return Response(data=payload, status=status.HTTP_200_OK)
