from django.contrib import admin

# Register your models here.
from .models import Category, Tage, Project, Picture, Comment, Reply, Donation, Rate, InAppropriateProject, \
    InAppropriateComment, InAppropriateReply

admin.site.register(Category)
admin.site.register(Tage)
admin.site.register(Project)
admin.site.register(Comment)
admin.site.register(Reply)
admin.site.register(Donation)
admin.site.register(Rate)
admin.site.register(InAppropriateProject)
admin.site.register(InAppropriateComment)
admin.site.register(InAppropriateReply)
admin.site.register(Picture)
