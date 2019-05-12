from django.shortcuts import render
from .formCreat import CreateProject
from django.http import HttpResponse


# Create your views here.
def index(request):
    return render(request, 'projects/index.html')


def project_details(request, _id):
    return render(request, 'projects/project_details.html')


def create(request):
    if request.method == 'POST':
        form = CreateProject(request.POST)
        if form.is_valid():
            return HttpResponse("Mission Complete")
    else:
        form = CreateProject()
        return render(request, 'projects/create.html', {'form': form})
