from django.core import paginator
from users.views import profiles
from projects.models import Project
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from .models import Project, Tags
from .forms import ProjectForm, ReviewForm
from .utils import searchProject, paginateProjects



def projects(request):
    projects, search_query = searchProject(request)
    custom_range, projects = paginateProjects(request, projects, 6)

    context = {'projects':projects, 'search_query': search_query, 'paginator': paginator, 'custom_range': custom_range}
    return render(request, 'projects/projects.html', context)


def viewProject(request, pk):
    project = Project.objects.get(id=pk)
    form = ReviewForm()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid:
            review = form.save(commit=False)
            review.project = project
            review.owner = request.user.profile
            review.save()
            # Update project votecount
            project.getVoteCount
            messages.success(request, 'Your review was sussesfully added!')
            return redirect('view-project', pk=project.id)
            
    context = {'project': project, 'form': form}
    return render(request, 'projects/single_page.html', context)


@login_required(login_url='login')
def createProject(request):
    form = ProjectForm()
    profile = request.user.profile
    
    if request.method == "POST":
        newtags = request.POST.get('newtags').replace(',', ' ').split()
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid:
            project = form.save(commit=False)
            project.owner = profile
            project.save()

            for tag in newtags:
                tag, created = Tags.objects.get_or_create(name=tag)
                project.tags.add(tag)
                
            return redirect('account')

    context = {'form': form}
    return render(request, 'projects/form.html', context)

@login_required(login_url='login')
def updateProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    form = ProjectForm(instance=project)

    if request.method == "POST":
        newtags = request.POST.get('newtags').replace(',', ' ').split()
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid:
            form.save()

            for tag in newtags:
                tag, created = Tags.objects.get_or_create(name=tag)
                project.tags.add(tag)

            return redirect('account')

    context = {'form': form, 'project': project}
    return render(request, 'projects/form.html', context)

@login_required(login_url='login')
def deleteProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    if request.method == 'POST':
        # print(project)
        project.delete()
        return redirect('account')

    context = {'object': project}
    return render(request, 'delete-template.html', context)


