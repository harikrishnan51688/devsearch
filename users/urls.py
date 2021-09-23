from django import urls
from django.urls.conf import path
from . import views

urlpatterns = [
    path('login/', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerUser, name='register'),
    
    path('account/', views.userAccount, name='account'),
    path('edit-profile/', views.editprofile, name='edit-profile'),

    path('', views.profiles, name='profiles'),
    path('profiles/<str:pk>/', views.userProfiles, name='user-profiles'),

    path('add-skill/', views.createSkill, name='add-skill'),
    path('edit-skill/<str:pk>/', views.editSkill, name='edit-skill'),
    path('delete-skill/<str:pk>/', views.deleteSkill, name='delete-skill'),

    path('inbox/', views.inbox, name='inbox'),
    path('message/<str:pk>/', views.viewMessage, name='view-message'),
    path('send-message/<str:pk>/', views.sendMessage, name='send-message'),
]