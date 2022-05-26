from datetime import date
import datetime
from rest_framework.generics import GenericAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from .models import *
from freelancer.models import *
from auth_app.models import User
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from auth_app.custom_permissions import *
from django.db.models import Q
from django.shortcuts import get_object_or_404

# Business Logics

class ClientProfile(GenericAPIView):
    permission_classes = [IsAuthenticated, IsClient]
    parser_classes = [JSONParser, FormParser, MultiPartParser]
    
    # register client
    def post(self, request):  
        user = request.user
        serializer = ClientSerializer(context= {'user':user}, data= request.data)
        if serializer.is_valid():    
            serializer.save()           
            return Response({              
                'data': 'updated profile Successfully !!',
                'status' : status.HTTP_200_OK })
        else:
            return Response({'data': 'Invalid Form !!', 'status': status.HTTP_400_BAD_REQUEST})

    def get(self, request):        
        user = request.user
        try:            
            client= Client.objects.get(user=user)   
            #photo_url = "http://localhost:8000/media/"                    
            payload = {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'phone': str(user.phone),
                'sex': client.sex,
                'location': client.location,
                'company': client.company,
                'photo': str(client.photo),
                'contribution': client.contribution,
                'is_verified': client.is_verified,            
            }
            return Response(data= payload, status= status.HTTP_200_OK, content_type="application/json")
        except Exception as e:
            return Response(data= 'Couldn\'t fetch !!', status= status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        user= request.user
        client= Client.objects.get(user=user)
        print(request.data)
        serializer = ClientSerializer(instance=client, data= request.data, context= {'user':user})
        user_serializer = UserUpdateSerializer(instance=user, data= request.data, context= {'user':user})
        if serializer.is_valid() and user_serializer.is_valid():
            serializer.save()
            user_serializer.save()
            return Response(data= 'updated profile Successfully !!', status= status.HTTP_200_OK)
        else:
            return Response(data= 'Invalid Form !!', status= status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        try:
            user= User.objects.get(user = request.user)            
            user.delete()            
            return Response(data= 'Account Deleted ....', status= status.HTTP_200_OK)
        except Exception as e:
            return Response(data= 'Something Went Wrong !!', status= status.HTTP_400_BAD_REQUEST)        
        

class JobCrud(GenericAPIView):
    permission_classes = [IsAuthenticated, IsClient]

    # add job
    def post(self, request):
        user = request.user
        print("request   ----", request.data)
        """ if Jobs.objects.filter(client=client).exists():
            return Response(data="Upgrade acount to add multiple jobs", status=status.HTTP_406_NOT_ACCEPTABLE)
        else: """
        serializer = JobSerializer(context= {'user':user}, data= request.data)    
        if serializer.is_valid():     
            serializer.save()
            return Response(data='Job added Successfully !!',status= status.HTTP_200_OK )
        else:
            return Response(data= 'Invalid Form !!', status= status.HTTP_400_BAD_REQUEST)

    # manage jobs
    def get(self, request):
        client = Client.objects.get(user= request.user)
        jobs = Jobs.objects.filter(Q(client=client) & Q(is_finished=False))    
        if jobs:
            payload= []  
            for job in jobs:          
                skills = Job_skills.objects.filter(job= job) 
                skill_list=[] 
                for skills in skills: 
                    skill_list = skill_list+[skills.skill]                             
                payload = payload + [{
                    'id':job.id,
                    'post_date':job.post_date,
                    'title': job.title,
                    'description': job.description,
                    'duration': job.duration,
                    'max_pay': job.max_pay,
                    'skill': skill_list }] 
            return Response(data = payload, status= status.HTTP_200_OK)
        else:
            return Response(data= 'No jobs yet....', status= status.HTTP_204_NO_CONTENT)

    def put(self, request, id):
        job = Jobs.objects.get(id= id)       
        serializer = JobSerializer(
            instance=job, context= {'user': request.user}, data=request.data) 
        if serializer.is_valid():
            serializer.save()
            return Response(data='Job updated Successfully !!', status = status.HTTP_200_OK)
        else:
            return Response(data= 'Invalid Form !!', status= status.HTTP_400_BAD_REQUEST)
            
    def delete(self, request, id):      
        try:      
            job = Jobs.objects.get(id= id)
            job.delete()
            return Response(data= 'Job deleted Successfully !!', status= status.HTTP_200_OK)
        except Exception as e:
            return Response(data= 'Couldn\'t delete !!', status= status.HTTP_400_BAD_REQUEST)


class JobSingleView(GenericAPIView):
    permission_classes = [IsAuthenticated, IsClient]

    def get(self, request, id):
        job = Jobs.objects.get(id= id)
        try:                                  
            payload = {
                'id':job.id,
                'post_date':job.post_date,
                'title': job.title,
                'description': job.description,
                'duration': job.duration,
                'max_pay': job.max_pay,
            }
            return Response(data = payload, status= status.HTTP_200_OK)
        except Exception as e:
            return Response(data= "Error in finding the excat job", status=status.HTTP_404_NOT_FOUND)

class Bid(GenericAPIView):
    permission_classes = [IsAuthenticated, IsClient]

    # pending requests
    def get(self, request): 
        client = Client.objects.get(user=request.user)
        rawJobs = Jobs.objects.filter(Q(client=client) & Q(is_finished=False))
        jobs = []
        for obj in rawJobs:
            if not Contract.objects.filter(job=obj).exists():
                jobs = jobs + [obj]
        if not jobs:   
            return Response(data= "No jobs Yet", status=status.HTTP_204_NO_CONTENT)
        else:
            print("JOBS ----",jobs)
            payload = []
            for job in jobs:
                bids = Bids.objects.filter(job=job)
                if bids:
                    print("bids -----", bids)
                    for bid in bids:
                        print("bid -----", bid)                
                        payload = payload + [{
                            'job_id': bid.job.id,
                            'bid_id': bid.id,
                            'fid': bid.freelancer.id,
                            'title': bid.job.title,
                            'description': bid.job.description,
                            'post_date': bid.job.post_date,
                            'duration': bid.job.duration,
                            'max_pay': bid.job.max_pay,
                            'freelancer': bid.freelancer.user.first_name + " " + bid.freelancer.user.last_name,
                            'amount':bid.amount,
                            'about': bid.about,
                            'bid_date': bid.bid_date
                        }]
                    print("payload ---- ",payload)
                    return Response(data = payload, status= status.HTTP_200_OK)
                else:
                    return Response(data= "No bids yet....", status= status.HTTP_204_NO_CONTENT)


class Contracts(GenericAPIView):
    permission_classes = [IsAuthenticated, IsClient]

    # select bid
    def post(self, request, id): 
        bid = Bids.objects.get(id=id)       
        freelancer = bid.freelancer
        job = bid.job
        end_date = date.today() + datetime.timedelta(job.duration)
        try: 
            Contract.objects.create(job=job, freelancer=freelancer, end_date= end_date)  
            freelancer.verified = True          
            if Favourites.objects.filter(job=job).exists():
                fav = Favourites.objects.get(job=job)
                fav.delete()
            return Response(data='contract initiated', status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data='something went wrong !!', status=status.HTTP_500_INTERNAL_SERVER_ERROR)  

    # current job
    def get(self, request):
        client = Client.objects.get(user=request.user)
        jobs = Jobs.objects.filter(Q(client=client) & Q(is_finished=False))
        print(jobs)
        payload = []
        if not jobs:
            return Response(data="NO job", status= status.HTTP_204_NO_CONTENT)
        else:
            for job in jobs:
                contract = Contract.objects.get(Q(job=job) & Q(submitted=False))
                #contract = get_object_or_404(Contract, job=job)
                if not contract:
                    return Response(data="NO contract", status= status.HTTP_204_NO_CONTENT)
                else:
                    print("contract inside --------------- ", contract)
                    bid = Bids.objects.get(Q(job=contract.job) & Q(freelancer=contract.freelancer))
                    print("bid : ",bid)
                    payload = payload + [{
                        'contract_id': contract.id,
                        'job_id': contract.job.id,
                        'title': contract.job.title,
                        'description': contract.job.description,
                        'post_date': contract.job.post_date,
                        'duration': contract.job.duration,
                        'max_pay': contract.job.max_pay,
                        'freelancer': contract.freelancer.user.first_name+" "+contract.freelancer.user.last_name,
                        'email': contract.freelancer.user.email,
                        'phone': str(contract.freelancer.user.phone),
                        'selected_bid': bid.amount,
                        'start_date': contract.start_date,
                        'deadline': contract.end_date
                    }]
                    return Response(data=payload, status= status.HTTP_200_OK)
            
    def delete(self, request, id):
        try:
            contract = Contract.objects.get(id=id)
            contract.delete()
            return Response(data= 'Contract cancelled Successfully !!', status= status.HTTP_200_OK)
        except Exception as e:
            return Response(data= 'Contract couldn\'t cancel !!', status= status.HTTP_400_BAD_REQUEST) 


class History(GenericAPIView):
    permission_classes=[IsAuthenticated, IsClient]

    # finish a contract 
    def post(self, request, id):       
        serializer = HistorySerializer(context={'id':id}, data=request.data)
        if serializer.is_valid():
            serializer.save()            
            return Response(data= 'Contract over Successfully !!', status= status.HTTP_200_OK)
        else:
            return Response(data= 'Something Went Wrong !!', status= status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # job history
    def get(self, request):
        client = Client.objects.get(user=request.user)
        jobs = Jobs.objects.filter(Q(client=client) & Q(is_finished=True))
        if not jobs:
            return Response(data="NO job", status= status.HTTP_204_NO_CONTENT)
        else:
            payload = []
            for job in jobs:
                print("JOBS : ",job)
                contract = Contract.objects.get(job=job)

                print("CONTRACT : ",contract)

                bid = Bids.objects.get(Q(job=contract.job) & Q(freelancer=contract.freelancer))
                print("BID : ", bid)
                payload = payload + [{
                    'job_id': contract.job.id,
                    'title': contract.job.title,
                    'description': contract.job.description,
                    'post_date': contract.job.post_date,
                    'start_date': contract.start_date,
                    'end_date': contract.end_date,
                    'freelancer': contract.freelancer.user.first_name+" "+contract.freelancer.user.last_name,
                    'bid': bid.amount,
                    'review': contract.review,
                }]
            return Response(data= payload, status= status.HTTP_200_OK)                    

            
class Freelancerprofile(GenericAPIView):
    permission_classes = [IsAuthenticated, IsClient]

    def get(self, request, id):
        try:  
            freelancer = Freelancer.objects.get(id=id)
            skills = Skills.objects.filter(freelancer=freelancer) 
            skill_list=[]
            for skills in skills: 
                skill_list = skill_list+ [{skills.id : skills.skill}]
            payload = {
            'id': freelancer.id,
            'first_name': freelancer.user.first_name,
            'last_name': freelancer.user.last_name,
            'email': freelancer.user.email,
            'phone': str(freelancer.user.phone),
            'tag': freelancer.tag,
            'sex': freelancer.sex,
            'dob': freelancer.dob,
            'location': freelancer.location,
            'qualification': freelancer.qualification,
            'experience': freelancer.experience,
            'photo': str(freelancer.photo),
            'contribution': freelancer.contribution,
            'is_verified': freelancer.is_verified,
            'ratings': freelancer.ratings,
            'skill': skill_list }
            print(payload)
            return Response(data= payload, status= status.HTTP_200_OK, content_type="application/json")
        except Exception as e:
            return Response(data= 'Couldn\'t fetch !!', status= status.HTTP_400_BAD_REQUEST)


class Recommend(GenericAPIView):
    permission_classes = [IsAuthenticated, IsClient]

    def get(self, request):
        client = Client.objects.get(user=request.user)
        jobs = Jobs.objects.filter(client=client)
        payload = []
        if jobs:
            for job in jobs:
                skills = Job_skills.objects.filter(job=job) # all job skills
                if skills:
                    for skill in skills:                
                        if Skills.objects.filter(skill__icontains=skill.skill).exists():
                            results = Skills.objects.filter(skill=skill.skill)                    
                            for result in results:
                                payload = payload + [{
                                    'fid': result.freelancer.id,
                                    'freelancer': result.freelancer.user.first_name+" "+result.freelancer.user.last_name, 
                                    'tag': result.freelancer.tag,
                                    'email': result.freelancer.user.email,
                                    'contribution': result.freelancer.contribution,
                                    'experience': result.freelancer.experience,
                                    'is_verified': result.freelancer.is_verified
                                }]
                        else:
                            freelancers = Freelancer.objects.all()[:4]
                            send_list = []
                            for freelancer in freelancers:
                                send_list = send_list+[{
                                    'fid': freelancer.id,
                                    'freelancer': freelancer.user.first_name+" "+freelancer.user.last_name, 
                                    'tag': freelancer.tag,
                                    'email': freelancer.user.email,
                                    'contribution': freelancer.contribution,
                                    'experience': freelancer.experience,
                                    'is_verified': freelancer.is_verified                            
                                }]
                            return Response(data=send_list, status= status.HTTP_200_OK)
                    return Response(data=payload, status=status.HTTP_200_OK)
                else:
                    freelancers = Freelancer.objects.all()[:4]
                    send_list = []
                    for freelancer in freelancers:
                        send_list = send_list+[{
                            'fid': freelancer.id,
                            'freelancer': freelancer.user.first_name+" "+freelancer.user.last_name,
                            'tag': freelancer.tag, 
                            'email': freelancer.user.email,
                            'contribution': freelancer.contribution,
                            'experience': freelancer.experience,
                            'is_verified': freelancer.is_verified                    
                        }]
                    return Response(data=send_list, status= status.HTTP_200_OK)            


class Search(GenericAPIView):
    permission_classes = [IsAuthenticated, IsClient]
    
    def post(self, request):
        search = request.data.get('search')
        skills =  Skills.objects.filter(skill__icontains = search)
        payload = []
        if skills:
            for skill in skills:
                payload = payload + [{
                    'fid': skill.freelancer.id,
                    'freelancer': skill.freelancer.user.first_name+" "+skill.freelancer.user.last_name, 
                    'tag': skill.freelancer.tag,
                    'email': skill.freelancer.user.email,
                    'contribution': skill.freelancer.contribution,
                    'experience': skill.freelancer.experience,
                    'is_verified': skill.freelancer.is_verified 
                }]
            return Response(data=payload, status=status.HTTP_200_OK)
        else:
            return Response(data=payload, status=status.HTTP_204_NO_CONTENT)
        





         