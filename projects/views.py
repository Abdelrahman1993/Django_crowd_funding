from django.shortcuts import get_object_or_404, render
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
    # print("===========================")
    # print(comment)
    return render(request, 'projects/project_details.html', {'project': project})
