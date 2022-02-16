from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from .models import *
from .serializers import *
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication

# Create your views here.

def index(request):
    return render(request, 'index.html')

class Routes(GenericAPIView):
    #permission_classes = [IsAuthenticated]

    def get(self, request):
        routes = {
            'login': 'api/login',
            'logout': 'api/logout',
            'register': 'api/register', 
            'refresh token': 'api/token/refresh',
                       
            'client profile post': "api/client/profile/post",
            'client profile get': 'api/client/profile/get',
            'client profile put': 'api/client/profile/put',
            'client profile delete': 'api/client/profile/delete',

            'freelancer profile post': "api/freelancer/profile/post",
            'freelancer profile get': "api/freelancer/profile/get",
            'freelancer profile put': "api/freelancer/profile/put",
            'freelancer profile delete': "api/freelancer/profile/delete",

            'job post': 'api/client/job/post',
            'job get': 'api/client/job/get',
            'job put': 'api/client/job/put/<int:id>',
            'job delete': 'api/client/job/delete/<int:id>',

            'current job': 'api/client/job/current',
            'pending requests': 'api/client/job/pending',
            'select bid': 'api/client/bid/select',
            'revoke bid': 'api/client/bid/revoke',
            'job history': 'api/client/job/history',

            'current contract': 'api/freelancer/contract/current',
            'favourite jobs': 'api/freelancer/job/favourite',
            'add favourite': 'api/freelancer/favourite/add',
            'remove favourite': 'api/freelancer/favourite/remove',
            'add bid': 'api/freelancer/bid/post',
            'applied bids': 'api/freelancer/bids/get',            
            'delete bid': 'api/freelancer/bid/delete',
            'contract history': 'api/freelancer/contract/history',

            'client search': 'api/client/search',
            'freelancer search': 'api/freelancer/search',

        }
        return Response(routes)        

class Register(GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = UserSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()        
            refresh = RefreshToken.for_user(request.user) 
            return Response({              
                'refresh' : str(refresh),
                'access' : str(refresh.access_token),
                'data': 'Registerd Successfully !!',
                'status' : status.HTTP_201_CREATED,
            })
        else:
            return Response(data= 'Invalid Form !!', status= status.HTTP_400_BAD_REQUEST)

""" class Login(GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception = True)
        email = request.data.get('email')
        user = User.objects.get(email = email)
        refresh = RefreshToken.for_user(user)        
        return Response({
            'refresh' : str(refresh),
            'access' : str(refresh.access_token),
            'data': 'Login Successfully !!',
            'status' : status.HTTP_200_OK,
        }) """

class Logout(GenericAPIView):
    authentication_classes = [JWTAuthentication]

    def post(self, request, format=None):
        try:
            refresh_token = request.data.get('refresh_token')
            #access_token = request.META.get('HTTP_AUTHORIZATION').split(" ")[1]
            token_obj = RefreshToken(refresh_token)  
            token_obj.blacklist()
            return Response(data= "Log out Successfully !!", status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data= "Something went Wrong !!", status=status.HTTP_404_NOT_FOUND)     
        
            

        
           
