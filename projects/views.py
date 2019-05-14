
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.http import HttpResponse
from .formCreat import CreateProject
from .models import Comment, Project, Reply, Picture, Category

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
        user_id=request.user.id, body=request.POST['body'],
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
    picture = Picture.objects.all().filter(project_id=project_id)
    return render(request, 'projects/edit_comment.html', {'project': project, 'comment_id': comment_id,'picture':picture[0]})


def update_comment(request, comment_id, project_id):
    body = request.POST['body']
    Comment.objects.filter(pk=comment_id).update(body=body)
    project = get_object_or_404(Project, pk=project_id)
    return redirect('projects:project_details', project_id=project_id)


def new_reply(request, comment_id, project_id):
    project = get_object_or_404(Project, pk=project_id)
    picture = Picture.objects.all().filter(project_id=project_id)
    return render(request, 'projects/new_reply.html', {'comment_id': comment_id, 'project': project,'picture':picture[0]})


def add_reply(request, comment_id, project_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    reply = Reply(
        user_id=request.user.id, body=request.POST['body'],
        comment_id=comment_id)
    reply.save()
    return redirect('projects:project_details', project_id=project_id)

def delete_reply(request, comment_id, project_id, reply_id):
    Reply.objects.filter(pk=reply_id).delete()
    project = get_object_or_404(Project, pk=project_id)
    return redirect('projects:project_details', project_id=project_id)


def edit_reply(request, comment_id, project_id, reply_id):
    project = Project.objects.get(pk=project_id)
    comment = Comment.objects.get(pk=comment_id)
    picture = Picture.objects.all().filter(project_id=project_id)
    return render(request, 'projects/edit_reply.html', {'project': project, 'comment_id':comment_id, 'reply_id': reply_id,'picture':picture[0]})


def update_reply(request, comment_id, project_id, reply_id):
    body = request.POST['body']
    Reply.objects.filter(pk=reply_id).update(body=body)
    project = get_object_or_404(Project, pk=project_id)
    return redirect('projects:project_details', project_id=project_id)


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
