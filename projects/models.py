from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from accounts.models import User
from taggit.managers import TaggableManager


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Tage(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Project(models.Model):
    title = models.CharField(max_length=200)
    details = models.TextField(blank=True)
    target = models.IntegerField()
    start_time = models.DateTimeField(auto_now_add=True, blank=True)
    end_time = models.DateTimeField()
    featured = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    tages = TaggableManager()

    class Meta:
        ordering = ('title',)

    def __str__(self):
        return self.title


# def get_image_filename(instance, filename):
#     id = instance.Project.id
#     return "post_images/%s" % (id)


class Picture(models.Model):
    image = models.ImageField(upload_to='photos/')
    project = models.ForeignKey(Project, on_delete=models.CASCADE)


class Comment(models.Model):
    body = models.TextField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Reply(models.Model):
    body = models.TextField()
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Donation(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.IntegerField()


class Rate(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rate = models.PositiveIntegerField(
        blank=True, validators=[MinValueValidator(1), MaxValueValidator(100)])


class InAppropriateProject(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    # is_appropriate = models.BooleanField()


class InAppropriateComment(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    # is_appropriate = models.BooleanField()


class InAppropriateReply(models.Model):
    reply = models.ForeignKey(Reply, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    # is_appropriate = models.BooleanField()
