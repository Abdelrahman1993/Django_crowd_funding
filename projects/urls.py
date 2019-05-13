from django.urls import path
from . import views
app_name='projects'
urlpatterns = [
    path('', views.index, name="index"),
    path('<int:project_id>/addComment', views.new_comment, name="addComment"),
    path('<int:project_id>/', views.project_details, name="project_details")
]