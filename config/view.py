from django.shortcuts import render, redirect
from django.http import HttpResponse


def root(request):
  if request.user.is_authenticated:
    return HttpResponse("your are logged in")
  else:
    return HttpResponse("not logged please login")
