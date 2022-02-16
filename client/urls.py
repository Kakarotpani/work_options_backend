from django.urls import path
from . views import *

urlpatterns = [
    path('profile/post', ClientProfile.as_view()),
    path('profile/get', ClientProfile.as_view()),
    path('profile/put', ClientProfile.as_view()),
    path('profile/delete', ClientProfile.as_view()),
    path('job/post', JobCrud.as_view()),
    path('job/get', JobCrud.as_view()),
    path('job/put/<int:id>', JobCrud.as_view()),
    path('job/delete/<int:id>', JobCrud.as_view()),
    path('contract/post/<int:id>', Contracts.as_view()),
    path('contract/get', Contracts.as_view()),
    path('contract/delete/<int:id>', Contracts.as_view()),
    path('bid/get', Bid.as_view()),
    path('history/post/<int:id>', History.as_view()),
    path('history/get', History.as_view()),
    path('bid/profile/get/<int:id>', Freelancerprofile.as_view()),
    path('recommend/get', Recommend.as_view()),
    path('search/get', Search.as_view()),
]  

