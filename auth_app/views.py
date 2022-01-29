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
    #authentication_classes = [JWTAuthentication]

    def get(self, request):
        routes = {
            'login': '/api/login',
            'refresh token': '/api/token/refresh',
            'register': 'api/register',
            'logout': '/logout',

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

    def get(self, request):
        try:
            refresh_token = request.data.get('refresh_token') or request.data.get('access_token')                        
            token_obj = RefreshToken(refresh_token)            
            token_obj.blacklist()
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
            

        

           
