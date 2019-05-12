from django.urls import path
from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_view

app_name = 'accounts'

urlpatterns = [
  path('login/', auth_view.LoginView.as_view(template_name='accounts/login.html'), name='login'),
  path('logout/', auth_view.LogoutView.as_view(), name='logout'),
  path('signup/', views.Signup.as_view(), name='signup'),
  path('activate/<str:uid>/<str:token>', views.Activate.as_view(), name='activate'),
  # url(r'^profile/(?P<pk>\d+)$', views.my_profile, name='my_profile'),
]
