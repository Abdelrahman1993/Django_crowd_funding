from django.urls import path
from . import views
app_name='projects'
urlpatterns = [
    path('', views.index, name="index"),
    path('create', views.create, name="create"),
    path('<int:_id>', views.project_details, name="project_details")
]