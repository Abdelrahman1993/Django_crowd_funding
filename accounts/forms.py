from django import forms
from django.contrib.auth.forms import UserCreationForm, get_user_model
from .models import User
from django.core.validators import RegexValidator


class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')

    phone_regex = RegexValidator(regex=r'^01[1|0|2|5][0-9]{8}$',
                                 message="Phone number must match egyptian format")
    phone = forms.CharField(validators=[phone_regex], max_length=11, min_length=11, required=True)

    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'email', 'phone', 'password1', 'password2', 'image')

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)


class EditProfileForm(forms.ModelForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone', 'facebook_profile', 'country', 'image')

    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['readonly'] = True
