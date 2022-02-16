from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# urls here.

urlpatterns = [    
    path('', views.Routes.as_view()),
    path('index', views.index),
    path('api/login', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register', views.Register.as_view()),
    path('api/logout', views.Logout.as_view()), # pass refresh_token in form-data 
]