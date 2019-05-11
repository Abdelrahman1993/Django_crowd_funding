from django.shortcuts import render
from django.http import HttpResponse
from projects.models import Project
# Create your views here.
def index(request):
    projects = Project.objects.all()[:5]
    highest_five_rated = Project.objects.all()[:5]
    latest_five = Project.objects.all()[:5]
    featured_five = Project.objects.all()[:5]
    #print (projects[0].picture_set.all)
    context = {
        'highest_five_rated': highest_five_rated ,
        'latest_five': latest_five,
        'featured_five': featured_five,
    }
    return render(request, 'pages/index.html', context)
