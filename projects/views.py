from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.http import HttpResponse
from .models import Comment, Project

# Create your views here.


def index(request):
    return render(request, 'projects/index.html')


def project_details(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    return render(request, 'projects/project_details.html', {'project': project})


def new_comment(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    comment = Comment(
        user_id=request.POST['user_id'], body=request.POST['body'],
        project_id=project_id)
    comment.save()
    return render(request, 'projects/project_details.html', {'project': project})


def delete_comment(request, comment_id, project_id):
    Comment.objects.filter(pk=comment_id).delete()
    project = get_object_or_404(Project, pk=project_id)
    return render(request, 'projects/project_details.html', {'project': project})


def edit_comment(request, comment_id, project_id):
    project = Project.objects.get(pk=project_id)
    comment = Comment.objects.get(pk=comment_id)
    return render(request, 'projects/edit_comment.html', {'project': project, 'comment_id': comment_id})


def update_comment(request, comment_id, project_id):
    body = request.POST['body']
    Comment.objects.filter(pk=comment_id).update(body=body)
    project = get_object_or_404(Project, pk=project_id)
    return render(request, 'projects/project_details.html', {'project': project})
