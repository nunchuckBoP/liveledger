from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django import forms
from django.forms import ValidationError

class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True,
                         label='Email',
                         error_messages={'exists': 'Oops, that email exists already..sorry.'})

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email']).exists():
            raise ValidationError(self.fields['email'].error_messages['exists'])
        return self.cleaned_data['email']

class UserProfileForm(UserChangeForm):
    first_name = forms.CharField(max_length=180)
    last_name = forms.CharField(max_length=180)
    email = forms.EmailField(max_length=180)

    class Meta:
        model = User
        fields = ['first_name','last_name', 'email']

    def clean_password(self):
        return self.clean_password()