from django.shortcuts import render
from .formCreat import CreateProject
from django.http import HttpResponse
from .models import Project, Category, Picture


# Create your views here.
def index(request):
    return render(request, 'projects/index.html')


def project_details(request, _id):
    return render(request, 'projects/project_details.html')


def create(request):
    category = Category.objects.all()
    if request.method == 'POST':
        form = CreateProject(request.POST)
        print("===================================")
        print(request.POST)
        print("===================================")
        print(request.POST['Images'])
        print("===================================")
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
                if request.POST['Images']:
                    picture = Picture()
                    picture.project_id = project.id
                    picture.image = request.POST['Images']
                    picture.save()
                    form = CreateProject()
                    if picture.id:
                        contextpost = {
                            'form': form,
                            'category': category,
                            'done': "broject has been created and picture saved"
                        }
                    else:
                        contextpost = {
                            'form': form,
                            'category': category,
                            'done': "broject has been created and picture dose not saved"
                        }
                    return render(request, 'projects/create.html', contextpost)
                return HttpResponse('nooooooooooooooooo')
        return HttpResponse(form.fields)
    else:
        form = CreateProject()
        contextget = {
            'form': form,
            'category': category,
        }
        return render(request, 'projects/create.html', contextget)
