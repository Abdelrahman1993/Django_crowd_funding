from django.views import View
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import SignupForm
from django.contrib.sites.shortcuts import get_current_site
from .models import User
from django.core.mail import EmailMessage
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import account_activation_token
from django.contrib.auth import authenticate, login, logout, password_validation
from django.contrib.auth.hashers import check_password


class Signup(View):
  def get(self, request):
    form = SignupForm()
    return render(request, 'accounts/signup.html', {'form': form})

  def post(self, request):
    form = SignupForm(request.POST)

    # print(form.cleaned_data['email'])
    if form.is_valid():
      # Create an inactive user with no password:
      user = form.save(commit=False)
      user.is_active = False
      # user.set_unusable_password()
      user.save()

      # Send an email to the user with the token:
      mail_subject = 'Activate your account.'
      current_site = get_current_site(request)
      uid = urlsafe_base64_encode(force_bytes(user.pk))
      token = account_activation_token.make_token(user)
      activation_link = "{0}/?uid={1}&token{2}".format(current_site, uid, token)
      message = "Hello {0},\n {1}".format(user.first_name + " " + user.last_name, activation_link)
      to_email = form.cleaned_data.get('email')
      email = EmailMessage(mail_subject, message, to=[to_email])
      email.send()
      return HttpResponse('Please confirm your email address to complete the registration')
    return redirect('accounts:signup', {form})


class Activate(View):
  def get(self, request, uidb64, token):
    try:
      uid = force_text(urlsafe_base64_decode(uidb64))
      user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
      user = None
    if user is not None and account_activation_token.check_token(user, token):
      # activate user and login:
      user.is_active = True
      user.save()
      return redirect('accounts:login')

    else:
      return HttpResponse('Activation link is invalid!')

  def post(self, request):
    form = PasswordChangeForm(request.user, request.POST)
    if form.is_valid():
      user = form.save()
      update_session_auth_hash(request, user)  # Important, to update the session with the new password
      return HttpResponse('Password changed successfully')


def user_login(request):
  if request.method == 'POST':
    email = request.POST.get('email')
    password = request.POST.get('password')
    user = User.objects.get(email__iexact=email)
    if user and user.check_password(password):
      if user:
        if user.is_active:
          login(request, user)
          next = request.POST.get('next', '/')
          return HttpResponseRedirect(next)
        else:
          return HttpResponse("Your account was inactive.")
      else:
        print("Someone tried to login and failed.")
        print("They used username: {} and password: {}".format(email, password))
        return HttpResponse("Invalid login details given")
    else:
      return HttpResponse("user not exist")
  else:
    return render(request, 'accounts/login.html', {})

# def my_profile(request, pk):
#   user = User.objects.filter(id=pk)[0]
#   questions = Question.objects.filter(status=True, receiver=user)
#   likes = []
#   like_count = 0
#   quest_count = len(questions)
#   for question in questions:
#     like = Like.objects.filter(user=request.user, question=question)
#     if like:
#       likes.append(1)
#       like_count += 1
#     else:
#       likes.append(0)
#   mylist = zip(questions, likes)
#   current_user = User.objects.get(username=request.user)
#
#   your_friend = False
#   friends = Friendship.objects.filter(creator=current_user)
#   for ff in friends:
#     if ff.friend == user:
#       your_friend = True
#
#   flag = True
#   if user == current_user:
#     flag = False
#
#   context = {
#     'your_friend': your_friend,
#     'flag': flag,
#     'questions': mylist,
#     'like_count': like_count,
#     'quest_count': quest_count,
#     'user': user,
#     'current_user': current_user,
#   }
#
#   return render(request, 'accounts/profile.html', context)
