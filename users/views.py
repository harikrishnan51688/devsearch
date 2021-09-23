from django.shortcuts import render, redirect
from django.contrib.auth import decorators, login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Profile, Message
from .utils import searchProfiles, paginateProfiles
from .forms import CustomUserCreationForm, ProfileForm, SkillForm, MessageForm

## Login and Register Section 

def loginUser(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('profiles')

    if request.method == "POST":
        username = request.POST['username'].lower()
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Username does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(request.GET['next'] if 'next' in request.GET else 'account')
        else:
            messages.error(request, 'Username or Password is incorrect')
    context = {'page':page}
    return render(request, 'users/login_register.html', context)

def logoutUser(request):
    logout(request)
    messages.info(request, 'User was logged out!')
    return redirect('login')

def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, "User account was created!")
            login(request, user)
            return redirect('edit-profile')

        else:
            messages.error(request, "An error occurred during registration")

    context = {'page':page, 'form':form}
    return render(request, 'users/login_register.html', context)

## Profile Section

def profiles(request):
    profiles, search_query = searchProfiles(request)
    custom_range , profiles = paginateProfiles(request, profiles, 6)

    context = {'profiles': profiles, 'search_query': search_query, 'custom_range': custom_range}
    return render(request, 'users/profiles.html', context)


def userProfiles(request, pk):
    profile = Profile.objects.get(id=pk)

    topskill = profile.skill_set.exclude(description__exact="")
    otherskill = profile.skill_set.filter(description="")

    context = {'profile':profile, 'topskill': topskill, 'otherskill': otherskill}
    return render(request, 'users/user-profile.html', context)


@login_required(login_url='login')
def userAccount(request):
    profile = request.user.profile
    skills = profile.skill_set.all()
    context = {'profile': profile, 'skills': skills,}
    return render(request, 'users/account.html', context)


@login_required(login_url='login')
def editprofile(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('account')

    context = {'form': form}
    return render(request, 'users/edit-profile.html', context)

## Skills Section

@login_required(login_url='login')
def createSkill(request):
    profile = request.user.profile
    form = SkillForm()

    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            messages.success(request, 'Skill was added succesfully')
            return redirect('account')
    context = {'form': form}
    return render(request, 'users/skill-form.html', context)


@login_required(login_url='login')
def editSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)

    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, 'Skill was updated succesfully')
            return redirect('account')
    context = {'form': form}
    return render(request, 'users/skill-form.html', context)


@login_required(login_url='login')
def deleteSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)

    if request.method == 'POST':
        skill.delete()
        messages.success(request, 'Skill was deleted succesfully')
        return redirect('account')
    context = {'object': skill}
    return render(request, 'delete-template.html', context)

## Message stuffs

@login_required(login_url='login')
def inbox(request):
    profile = request.user.profile
    messageRequests = profile.messages.all()
    unreadCount = messageRequests.filter(is_read=False).count()
    context = {'messageRequests': messageRequests, 'unreadCount': unreadCount}
    return render(request, 'users/inbox.html', context)

@login_required(login_url='login')
def viewMessage(request, pk):
    profile = request.user.profile
    message = profile.messages.get(id=pk)
    if message.is_read == False:
        message.is_read = True
        message.save()
    context = {'message': message}
    return render(request, 'users/message.html', context)


def sendMessage(request, pk):
    form = MessageForm()
    recipient = Profile.objects.get(id=pk)
    
    try:
        sender = request.user.profile
    except:
        sender = None


    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient

            if sender:
                message.name = sender.name
                message.email = sender.email
            message.save()

            messages.success(request, 'Your message was succesfully sent!')
            return redirect('user-profiles', pk=recipient.id)


    context = {'recipient': recipient, 'form': form}
    return render(request, 'users/message_form.html', context)
