from django.views import View
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import SignupForm, EditProfileForm
from django.contrib.sites.shortcuts import get_current_site
from .models import User
from django.core.mail import EmailMessage
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import account_activation_token
from django.contrib.auth import authenticate, login, logout, password_validation
from projects.models import Donation, Project, Tage
from django.views.generic import UpdateView
from django.urls import reverse_lazy


class Signup(View):
    def get(self, request):
        form = SignupForm()
        return render(request, 'accounts/signup.html', {'form': form})

    def post(self, request):
        form = SignupForm(request.POST)
        if form.is_valid():
            # Create an inactive user with no password:
            user = form.save(commit=False)
            user.image = request.FILES['image']
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
        if not user:
            return HttpResponse("user not exist")
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
        return render(request, 'accounts/login.html', {})


def my_profile(request, pk):
    user = User.objects.filter(id=pk)[0]
    my_projects = Project.objects.filter(user=request.user)
    my_donations = Donation.objects.filter(user=request.user)
    for i in my_projects:
        i.tags = Tage.objects.filter(project=i.id)

    context = {
        'user': user,
        'projects': my_projects,
        'donations': my_donations,
    }

    return render(request, 'accounts/profile.html', context)


# edit user profile
class Edit_profile(UpdateView):
    form_class = EditProfileForm
    template_name = 'accounts/edit_profile.html'

    def get_success_url(self):
        return reverse_lazy('accounts:my_profile', kwargs={'pk': self.kwargs['pk']})

    def get_object(self, queryset=None):
        obj = User.objects.get(id=self.kwargs['pk'])
        return obj


def warn(request):
    context = {
        'cancel': 'accounts:my_profile',
        'delete': 'accounts:delete_account',
        'msg': 'Are you sure you want to delete your account ? All your projects and donations will be deleted',
        'cancel_id': request.user.id,
        'delete_id': request.user.id,
    }
    return render(request, 'accounts/warn.html', context)


def delete_account(request, pk):
    user = User.objects.get(id=pk);
    logout(request)
    user.delete()
    return redirect('pages:index')
