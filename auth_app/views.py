from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from .models import *
from .serializers import *
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.token_blacklist.models import *

# Business Logics

def index(request):
    return render(request, 'index.html')

class Routes(GenericAPIView):
    #permission_classes = [IsAuthenticated]
    def get(self, request):
        routes = {
            "login_api": "api/login",
            "logout_api": "api/logout",
            "register_api": "api/register",
            "refresh_token_api": "api/token/refresh",
            "freelancer_profile_post": "api/freelancer/profile/post",
            "freelancer_profile_get": "api/freelancer/profile/get",
            "freelancer_profile_put": "api/freelancer/profile/put",
            "freelancer_profile_delete": "api/freelancer/profile/delete",

            "skill_post": "api/freelancer/skill/post",
            "skill_get": "api/freelancer/skill/get",
            "skill_put": "api/freelancer/skill/put/<int:id>",
            "skill_delete": "api/freelancer/skill/delete/<int:id>",

            "freelancer_bid_post" : "api/freelancer/bid/post/<int:id>",
            "freelancer_bid_get" : "api/freelancer/bid/get",
            "freelancer_bid_put" : "api/freelancer/bid/put/<int:id>",
            "freelancer_bid_delete" : "api/freelancer/bid/delete/<int:id>",

            "freelancer_favourite_post" : "api/freelancer/favourite/post/<int:id>",
            "freelancer_favourite_get" : "api/freelancer/favourite/get",
            "freelancer_favourite_delete" : "api/freelancer/favourite/delete/<int:id>",

            "freelancer_contract_get" : "api/freelancer/contract/get",
            "freelancer_history_get" : "api/freelancer/history/get",
            "bid_clientprofile_get": "api/freelancer/bid/profile/get/<int:id>",

            "freelancer_recommend": "api/freelancer/recommend/get",
            "freelancer_search": "api/freelancer/search",
            
            "client_profile_post": "api/client/profile/post",
            "client_profile_get": "api/client/profile/get",
            "client_profile_put": "api/client/profile/put",
            "client_profile delete": "api/client/profile/delete",

            "job_post": "api/client/job/post",
            "job_get": "api/client/job/get",
            "job_single_get": "api/client/job/single/get/<int:id>",
            "job_put": "api/client/job/put/<int:id>",
            "job_delete": "api/client/job/delete/<int:id>",

            "contract_post": "api/client/contract/post/<int:id>",
            "contract_get": "api/client/contract/get",
            "contract_delete": "api/client/contract/get",

            "history_post": "api/client/history/post/<int:id>",
            "history_get": "api/client/history/get",

            "bid_get": "api/client/bid/get",
            "bid_freelancerprofile_get": "api/client/bid/profile/get/<int:id>",

            "client_recommend": "api/client/recommend/get",
            "client_search": "api/client/search",
        }
        return Response(routes)        

class Register(GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = UserSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()    
            return Response({                              
                'status' : status.HTTP_201_CREATED,
            })
        else:
            return Response(data= 'Invalid Form !!', status= status.HTTP_400_BAD_REQUEST)
            
"""refresh = RefreshToken.for_user(request.user) 
    'refresh' : str(refresh),
    'access' : str(refresh.access_token),
    'data': 'Registerd Successfully !!', """

class Login(GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception = True)
        email = request.data.get('email')
        user = User.objects.get(email = email)
        refresh = RefreshToken.for_user(user)   
        return Response({
            'refresh_token' : str(refresh),
            'access_token' : str(refresh.access_token),
            'is_freelancer': user.is_freelancer,
            'is_client': user.is_client,
            'status' : status.HTTP_200_OK,
        })

class Logout(GenericAPIView):
    authentication_classes = [JWTAuthentication]

    def post(self, request, format=None):
        try:
            #pass 'refresh_token' key inside body
            #access_token = request.META.get('HTTP_AUTHORIZATION').split(" ")[1]
            refresh_token = request.data.get('refresh_token')
            refresh_obj = RefreshToken(refresh_token)
            refresh_obj.blacklist()

            #to flush all token data
            """ tokens = OutstandingToken.objects.filter(user=request.user)
            for token in tokens:
                _, _ = BlacklistedToken.objects.get_or_create(token=token) """
            
            return Response(data= "Log out Successfully !!", status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data= "Something went Wrong !!", status=status.HTTP_404_NOT_FOUND)     
        
            

        
           
