from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.http import HttpResponse
from .formCreat import CreateProject
from .models import Comment, Project, Reply, Picture, Category, Donation, InAppropriateProject, InAppropriateComment, InAppropriateReply

from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.core.paginator import Paginator

# Create your views here.


def index(request):
    projects_list = Project.objects.all()
    paginator = Paginator(projects_list, 9)
    page = request.GET.get('page')
    projects = paginator.get_page(page)
    report_projects = InAppropriateProject.objects.filter(
        user_id=request.user.id)
    print("====================")
    print(report_project)
    context = {
        'projects': projects,
        'report_projects': report_projects,
    }
    return render(request, 'projects/index.html', context)


def project_details(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    picture = Picture.objects.all().filter(project_id=project_id)

    report_projects = InAppropriateProject.objects.filter(
        user_id=request.user.id, project_id=project_id)

    report_comments = InAppropriateComment.objects.filter(
        user_id=request.user.id).values("comment_id")

    report_replies = InAppropriateReply.objects.filter(
        user_id=request.user.id).values("reply_id")
    print("*************")
    report_comment_ids = []
    report_reply_ids = []
    for c in report_comments:
        report_comment_ids.append(c['comment_id'])
    for r in report_replies:
        report_reply_ids.append(r['reply_id'])
    print(report_comment_ids)
    print(report_reply_ids)
    donations = Donation.objects.all().filter(project_id=project_id)
    reached_target = Donation.objects.filter(
        project_id=project_id).aggregate(total=Sum('amount'))
    print(reached_target)
    if reached_target['total']:
        percent = round(reached_target['total']*100/project.target, 2)
    else:
        percent = 0

    return render(request, 'projects/project_details.html', {
        'project': project,
        'picture': picture[0],
        'donations': donations,
        'percent': percent,
        'report_projects': report_projects,
        'report_comment_ids': report_comment_ids,
        'report_reply_ids': report_reply_ids
    })


def new_comment(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    comment = Comment(
        user_id=request.user.id,
        body=request.POST['body'],
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
    return render(request, 'projects/edit_comment.html', {'project': project, 'comment_id': comment_id, 'picture': picture[0]})


def update_comment(request, comment_id, project_id):
    body = request.POST['body']
    Comment.objects.filter(pk=comment_id).update(body=body)
    project = get_object_or_404(Project, pk=project_id)
    return redirect('projects:project_details', project_id=project_id)


def new_reply(request, comment_id, project_id):
    project = get_object_or_404(Project, pk=project_id)
    picture = Picture.objects.all().filter(project_id=project_id)
    report_comments = InAppropriateComment.objects.filter(
        user_id=request.user.id).values("comment_id")

    report_replies = InAppropriateReply.objects.filter(
        user_id=request.user.id).values("reply_id")
    report_comment_ids = []
    report_reply_ids = []
    for c in report_comments:
        report_comment_ids.append(c['comment_id'])
    for r in report_replies:
        report_reply_ids.append(r['reply_id'])
    return render(request, 'projects/new_reply.html',
                  {'comment_id': comment_id,
                   'project': project,
                   'picture': picture[0],
                   'report_comment_ids': report_comment_ids,
                   'report_reply_ids': report_reply_ids})


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

    report_replies = InAppropriateReply.objects.filter(
        user_id=request.user.id).values("reply_id")
    report_reply_ids = []
    for r in report_replies:
        report_reply_ids.append(r['reply_id'])

    return render(request, 'projects/edit_reply.html',
                 {'project': project,
                  'comment_id': comment_id,
                   'reply_id': reply_id,
                   'picture': picture[0],
                   'report_reply_ids': report_reply_ids
                   })


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


def donate(request, project_id):
    if request.POST.get('donation'):
        project = get_object_or_404(Project, pk=project_id)
        donation = Donation(
            user_id=request.user.id,
            amount=request.POST['donation'],
            project_id=project_id)
        donation.save()
        return redirect('projects:project_details', project_id=project_id)
    else:
        return redirect('projects:project_details', project_id=project_id)


def report_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    in_appropriate_project = InAppropriateProject(
        user_id=request.user.id,
project_id=project_id)
    in_appropriate_project.save()
    return redirect('projects:index')


def report_comment(request, project_id, comment_id):
    # project = get_object_or_404(Project, pk=project_id)
    in_appropriate_comment = InAppropriateComment(
        user_id=request.user.id,
        comment_id=comment_id)
    in_appropriate_comment.save()
    return redirect('projects:project_details', project_id=project_id)


def report_reply(request, project_id, comment_id, reply_id):
    # project = get_object_or_404(Project, pk=project_id)
    in_appropriate_reply = InAppropriateReply(
        user_id=request.user.id,
        reply_id=reply_id)
    in_appropriate_reply.save()
    return redirect('projects:project_details', project_id=project_id)


def warn(request, pk):
  context = {
    'cancel': 'projects:project_details',
    'delete': 'projects:project_delete',
    'msg': 'Are you sure you want to delete this project ? All it\'s donations, comments will be deleted',
    'cancel_id': pk,
    'delete_id': pk,
  }
  return render(request, 'accounts/warn.html', context)


def delete_project(request, pk):
  project = Project.objects.get(id=pk);
  project.delete()
  return redirect('pages:index')