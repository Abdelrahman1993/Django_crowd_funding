from django.shortcuts import render
from django.http import HttpResponse
from projects.models import Project
from django.db.models import Q
from django.contrib.auth.decorators import login_required


def index(request):
    #print(request.user)
    projects = Project.objects.all()[:5]
    highest_five_rated = Project.objects.all()[:5]
    latest_five = Project.objects.order_by('-start_time')[:5]
    featured_five = Project.objects.filter(featured = True)
    #print (projects[0].picture_set.all)
    context = {
        'highest_five_rated': highest_five_rated ,
        'latest_five': latest_five,
        'featured_five': featured_five,
    }
    return render(request, 'pages/index.html', context)

def search(request):
    if request.GET.get("search"):

        search_keyword = request.GET.get("search")
        # search_set3 = Project.objects.filter(title__icontains = search_keyword).distinct()
        # search_set2 = Project.objects.filter(tage__name__icontains = search_keyword).distinct()
        search_set = Project.objects.filter(Q(title__icontains = search_keyword) | Q(tage__name__icontains = search_keyword)).distinct()
        # return HttpResponse(search_set)
        context = {
            "projects_search": search_set
        }
        return render(request, 'pages/index.html',context)
    else:
         return render(request, 'pages/index.html')
