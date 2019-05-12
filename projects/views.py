from django.shortcuts import render
from .formCreat import CreateProject
from django.http import HttpResponse
from .models import Project, Category


# Create your views here.
def index(request):
    return render(request, 'projects/index.html')


def project_details(request, _id):
    return render(request, 'projects/project_details.html')


def create(request):
    if request.method == 'POST':
        form = CreateProject(request.POST)
        if form:
            project = Project()
            project.title = form['title'].value()
            project.target = int(form['target'].value())
            project.details = form['details'].value()
            project.end_time = form['endTiem'].value()
            project.category_id = int(request.POST['category'])
            project.tages = form['tages'].value()
            project.save()
            if project.id:
                form = CreateProject()
                category = Category.objects.all()
                context = {
                    'form': form,
                    'category': category,
                    'done': "broject has been created"
                }
                return render(request, 'projects/create.html', context)
            return HttpResponse('nooooooooooooooooo')
        return HttpResponse(form.fields)
    else:
        form = CreateProject()
        category = Category.objects.all()
        context = {
            'form': form,
            'category': category
        }
        return render(request, 'projects/create.html', context)
