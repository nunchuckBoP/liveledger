from django.shortcuts import get_object_or_404, redirect, render
from accounts.forms import UserCreateForm, UserProfileForm
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.base import TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.models import User

# Create your views here.
class SignUpView(CreateView):
    form_class = UserCreateForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

class UserProfileView(TemplateView):
    success_url = reverse_lazy('ledger-list')
    template_name = 'registration/profile.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return render(request, self.template_name, self.get_context_data(**kwargs))
        else:
            return redirect(reverse_lazy('login'))

    def get_context_data(self, **kwargs):
        object = get_object_or_404(User, pk=self.request.user.id)
        form = UserProfileForm(initial=object)
        return {"form":form, "object":object}