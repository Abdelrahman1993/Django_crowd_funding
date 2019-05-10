from django.shortcuts import render
from django.http import HttpResponse
from projects.models import Project
# Create your views here.
def index(request):
    projects = Project.objects.all()
    #print (projects[0].picture_set.all)
    context = {
        'projects': projects
    }
    return render(request, 'pages/index.html', context)
