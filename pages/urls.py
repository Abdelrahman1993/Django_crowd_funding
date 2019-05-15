from django.urls import path, include
from . import views

app_name = 'pages'

urlpatterns = [
    path('projects/', include('projects.urls')),
    path('', views.index, name="index"),
    path('search', views.search, name="search")
]