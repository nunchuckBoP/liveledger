from django.shortcuts import get_object_or_404, redirect, render
from accounts.forms import UserCreateForm, UserProfileForm
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.models import User

# Create your views here.
class SignUpView(CreateView):
    form_class = UserCreateForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

class UserChangeView(UpdateView):
    form_class = UserProfileForm
    model = User
    success_url = reverse_lazy('ledger-list')
    template_name = 'registration/profile.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super(UserChangeView, self).get(request, *args, **kwargs)
        else:
            return redirect(reverse_lazy('login'))

    def get_context_data(self, **kwargs):
        print("GOT HERE 2")
        #object = get_object_or_404(User, pk=self.request.user.id)
        #return {'object':object}