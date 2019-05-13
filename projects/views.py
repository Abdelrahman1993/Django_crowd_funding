from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.http import HttpResponse
from .models import Comment, Project, Reply, Picture

# Create your views here.


def index(request):
    return render(request, 'projects/index.html')


def project_details(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    picture = Picture.objects.all().filter(project_id=project_id)
    print("===================")
    current_user = request.user
    print(current_user.id)
    return render(request, 'projects/project_details.html', {'project': project,'picture':picture[1]})


def new_comment(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    comment = Comment(
        user_id=request.user, body=request.POST['body'],
        project_id=project_id)
    comment.save()
    return redirect('projects:project_details', project_id=project_id)


def delete_comment(request, comment_id, project_id):
    Comment.objects.filter(pk=comment_id).delete()
    project = get_object_or_404(Project, pk=project_id)
    return redirect('projects:project_details', project_id=project_id)


def edit_comment(request, comment_id, project_id):
    project = Project.objects.get(pk=project_id)
    comment = Comment.objects.get(pk=comment_id)
    return render(request, 'projects/edit_comment.html', {'project': project, 'comment_id': comment_id})


def update_comment(request, comment_id, project_id):
    body = request.POST['body']
    Comment.objects.filter(pk=comment_id).update(body=body)
    project = get_object_or_404(Project, pk=project_id)
    return redirect('projects:project_details', project_id=project_id)


def new_reply(request, comment_id, project_id):
    project = get_object_or_404(Project, pk=project_id)
    return render(request, 'projects/new_reply.html', {'comment_id': comment_id, 'project': project})


def add_reply(request, comment_id, project_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    reply = Reply(
        user_id=request.user, body=request.POST['body'],
        comment_id=comment_id)
    reply.save()
    return redirect('projects:project_details', project_id=project_id)
