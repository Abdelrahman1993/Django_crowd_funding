from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request, 'projects/index.html')

def project_details(request, _id):
    return render(request, 'projects/project_details.html')
