from django.shortcuts import render
from accounts.forms import UserCreateForm
from django.views import generic
from django.urls import reverse_lazy

# Create your views here.
class SignUpView(generic.CreateView):
    form_class = UserCreateForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'