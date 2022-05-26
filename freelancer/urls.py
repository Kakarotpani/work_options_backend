from django.urls import path
from .views import *

urlpatterns = [
    path('profile/post', FreelancerProfile.as_view()),
    path('profile/get', FreelancerProfile.as_view()),
    path('profile/put', FreelancerProfile.as_view()),
    path('profile/delete', FreelancerProfile.as_view()),
    path('skill/post', Skill.as_view()),
    path('skill/get', Skill.as_view()),
    path('skill/put/<int:id>', Skill.as_view()),
    path('skill/delete/<int:id>', Skill.as_view()),
    path('bid/post/<int:id>', Bid.as_view()),
    path('bid/get', Bid.as_view()),
    path('bid/put/<int:id>', Bid.as_view()),
    path('bid/delete/<int:id>', Bid.as_view()),
    path('favourite/post/<int:id>', Favourite.as_view()),
    path('favourite/get', Favourite.as_view()),
    path('favourite/delete/<int:id>', Favourite.as_view()),
    path('contract/get', Contracts.as_view()),
    path('history/get', History.as_view()),
    path('bid/profile/get/<int:id>', ClientProfile.as_view()),
    path('recommend/get', Recommend.as_view()),
    path('search/post', Search.as_view()),
]
