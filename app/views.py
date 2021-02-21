from django.http.response import HttpResponse
from django.urls import reverse_lazy
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.urls.base import reverse
from django.views.generic.base import RedirectView, TemplateView
from django.views.generic.list import ListView
from django.views.generic import CreateView, UpdateView, FormView
from django.views.generic.detail import DetailView
from django.views.generic import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.contrib.auth.models import User
from app.models import Ledger, LedgerItem
import app.forms
import app.mixins

class HomeView(TemplateView):
    template_name = "home.html"

class ForbiddenView(TemplateView):
    template_name = "forbidden.html"

# Create your views here.
class LedgerListView(LoginRequiredMixin, ListView):
    model = Ledger
    paginate_by = 100

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        if self.request.user.is_authenticated:
            objects = Ledger.objects.filter(
                            Q(created_by=self.request.user) | Q(shared_with=self.request.user)
                        ).order_by('description')
            context['objects'] = objects

            return context
        else:
            redirect(reverse_lazy('login'))

class LedgerCreateView(LoginRequiredMixin, CreateView):
    model = Ledger
    template_name = 'ledger_form.html'
    fields = ['description']
    success_url = reverse_lazy('ledger-list')
    heading_text = "Create Ledger"
    button_text = "Create Ledger"

    def form_valid(self, form):

        # gets the cleaned data
        self.object = form.save(commit=False)

        # adds the current user to acess the created
        # ledger
        self.object.created_by = self.request.user

        # save the object to the database
        self.object.save()

        return super(LedgerCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(LedgerCreateView, self).get_context_data(**kwargs)
        context['heading_text'] = self.heading_text
        context['button_text'] = self.button_text
        return context

class LedgerUpdateView(LoginRequiredMixin, UpdateView):
    model = Ledger
    template_name = 'ledger_form.html'
    fields = ['description']
    success_url = reverse_lazy('ledger-list')
    heading_text = 'Update Ledger'
    button_text = 'Save'

    def get_context_data(self, **kwargs):
        context = super(LedgerUpdateView, self).get_context_data(**kwargs)
        context['heading_text'] = self.heading_text
        context['button_text'] = self.button_text
        return context

class LedgerSharedUserRemoveView(LoginRequiredMixin, TemplateView):
    
    def get(self, request, *args, **kwargs):

        # get the ledger object
        ledger = get_object_or_404(Ledger, pk=kwargs.get('pk'))

        # get the user object
        user = get_object_or_404(User, username=kwargs.get('username'))

        if user in ledger.shared_with.all():
        
            # remove the user from the shared_with
            ledger.shared_with.remove(user)
            
            # save the ledger
            ledger.save()

        # return to the sucess url
        return redirect(reverse_lazy('ledger-share', kwargs={'pk':ledger.pk}))

class LedgerSharedRemoveMeView(LoginRequiredMixin, TemplateView):

    def get(self, request, *args, **kwargs):

        ledger = get_object_or_404(Ledger, pk=kwargs.get('pk'))

        if self.request.user in ledger.shared_with.all():

            # remove the user from the ledger
            ledger.shared_with.remove(self.request.user)

            # save the ledger
            ledger.save()

        return redirect(reverse_lazy('ledger-list'))
        

class LedgerShareView(LoginRequiredMixin, FormView):
    form_class = app.forms.LedgerShareForm
    template_name = 'ledger_shareform.html'
    success_url = reverse_lazy('ledger-list')
    heading_text = "Share Ledger"
    button_text = "Submit"
    fields = ['shared_with']

    def get_success_url(self):
        self.success_url = reverse_lazy('ledger-share', kwargs={'pk':self.kwargs.get('pk')})
        return self.success_url

    def get_context_data(self, **kwargs):
        context = super(LedgerShareView, self).get_context_data(**kwargs)
        context['object'] = get_object_or_404(Ledger, pk=self.kwargs['pk'])
        context['heading_text'] = self.heading_text
        context['button_text'] = self.button_text
        return context

    def form_valid(self, form): 
        # This method is called when valid form data has been POSTed. 
        # It should return an HttpResponse.
        shared_user = form.cleaned_data['shared_user']

        # we should only get one user object in this. It also should be a 
        # valid user because we validated that in the validator routine.
        user = User.objects.filter(Q(username=shared_user) | Q(email=shared_user))[0]

        # add it to the shared users for the ledger
        ledger = get_object_or_404(Ledger, pk=self.kwargs['pk'])

        # add the user to the shared_with group. does not add the user if they
        # are already added. Also, won't add the user that created the ledger
        # to the shared users.
        if user not in ledger.shared_with.all() and self.request.user != user:
            ledger.shared_with.add(user)

            # save the ledger object
            ledger.save()

        # return the super routine 
        return super().form_valid(form)

class LedgerDeleteView(LoginRequiredMixin, DeleteView):
    model = Ledger
    success_url = reverse_lazy('ledger-list')
    template_name = "confirm.html"
    heading_text = "Confirm Ledger Delete"
    button_text = "Delete"

    def get_context_data(self, **kwargs):
        context = super(LedgerDeleteView, self).get_context_data(**kwargs)
        context['heading_text'] = self.heading_text
        context['button_text'] = self.button_text
        return context

class LedgerItemListview(LoginRequiredMixin, ListView):
    model = LedgerItem
    queryset = LedgerItem.objects.all()

    def get_context_data(self, **kwargs):

        context = super(LedgerItemListview, self).get_context_data(**kwargs)
        ledger = get_object_or_404(Ledger, pk=self.kwargs['ledgerid'])
        if ledger.created_by == self.request.user or \
            self.request.user in ledger.shared_with.all():
            object_list = LedgerItem.objects.filter(ledger=ledger).order_by('created_on')
            context['ledger'] = ledger
            context['object_list'] = object_list
            return context
        else:
            return HttpResponseForbidden("User does not have access to ledger.")
        
class LedgerItemCreateView(LoginRequiredMixin, CreateView):
    model = LedgerItem
    template_name = 'ledger_form.html'
    fields = ['description', 'income', 'amount']
    success_url = reverse_lazy('ledgeritem-list')
    heading_text = "Create Ledger List Item"
    button_text = "Save Item"

    def get_success_url(self):
        if 'ledgerid' in self.kwargs:
            return reverse_lazy('ledgeritem-list', kwargs={'ledgerid':self.kwargs['ledgerid']})
        else:
            return reverse_lazy('ledger-list')

    def get(self, request, *args, **kwargs):
        self.ledger = get_object_or_404(Ledger, pk=kwargs['ledgerid'])
        if self.ledger.created_by == self.request.user or \
            self.request.user in self.ledger.shared_with.all():
            return super(LedgerItemCreateView, self).get(request, *args, **kwargs)
        else:
            return redirect(reverse_lazy('forbidden'))

    def get_context_data(self, **kwargs):
        context = super(LedgerItemCreateView, self).get_context_data(**kwargs)
        context['heading_text'] = self.heading_text
        context['button_text'] = self.button_text
        return context

    def form_valid(self, form):

        # gets the cleaned data
        self.object = form.save(commit=False)

        # gets the ledger object
        self.ledger = get_object_or_404(Ledger, pk=self.kwargs['ledgerid'])

        # make sure the user has access to the ledger
        if self.ledger.created_by == self.request.user or \
            self.request.user in self.ledger.shared_with.all():
        
            # adds the current user to acess the created
            # ledger
            self.object.created_by = self.request.user
            self.object.ledger = self.ledger

            # save the object to the database
            self.object.save()

            return super(LedgerItemCreateView, self).form_valid(form)
        else:
            return redirect(reverse_lazy('forbidden'))

class LedgerItemDeleteView(LoginRequiredMixin, DeleteView):
    model = LedgerItem
    template_name = 'confirm.html'
    success_url = reverse_lazy('ledgeritem-list')
    heading_text = "Confirm Deletion"
    message_text = "Are you sure that you want to delete this item?"
    button_text = "Delete"

    def checkuseraccess(self, User, LedgerItem):
        # get the ledger object
        self.ledger = LedgerItem.ledger

        # make sure the user has access to it
        if self.ledger.created_by == User or \
            User in self.ledger.shared_with.all():
            return True
        else:
            return False

    def get_success_url(self):
        return reverse_lazy('ledgeritem-list', kwargs={'ledgerid':self.object.ledger.pk})

    def get_context_data(self, **kwargs):

        if self.checkuseraccess(self.request.user, self.object):
            context = super(LedgerItemDeleteView, self).get_context_data(**kwargs)
            context['heading_text'] = self.heading_text
            context['message_text'] = self.message_text
            context['button_text'] = self.button_text
            return context
        else:
            return redirect(reverse_lazy('forbidden'))

class LedgerItemUpdateView(LoginRequiredMixin, UpdateView):
    model = LedgerItem
    template_name = 'ledger_form.html'
    fields = ['description', 'income', 'amount']
    success_url = reverse_lazy('ledgeritem-list')
    heading_text = "Update Ledger List Item"
    button_text = "Save Item"

    def checkuseraccess(self, User, LedgerItem):

        # get the ledger object
        self.ledger = LedgerItem.ledger

        # make sure the user has access to it
        if self.ledger.created_by == User or \
            User in self.ledger.shared_with.all():
            return True
        else:
            return False

    def get(self, request, *args, **kwargs):
        
        self.ledgeritem = get_object_or_404(LedgerItem, pk=kwargs['pk'])
        if self.checkuseraccess(request.user, self.ledgeritem):
            return super(LedgerItemUpdateView, self).get(request, *args, **kwargs)
        else:
            return redirect(reverse_lazy('forbidden'))

    def get_success_url(self):
        return reverse_lazy('ledgeritem-list', kwargs={'ledgerid':self.object.ledger.pk})

    def get_context_data(self, **kwargs):
        context = super(LedgerItemUpdateView, self).get_context_data(**kwargs)
        context['heading_text'] = self.heading_text
        context['button_text'] = self.button_text
        return context

    def form_valid(self, form):

        # make sure the user has access to the ledger
        if self.checkuseraccess(self.request.user, self.object):
            return super(LedgerItemUpdateView, self).form_valid(form)
        else:
            return redirect(reverse_lazy('forbidden'))

class LedgerItemInquireView(LoginRequiredMixin, FormView):
    
    form_class = app.forms.InquireForm
    success_url = reverse_lazy('ledger-list')
    template_name = "inquire_form.html"
    heading_text = "Inquire on Ledger Item"
    button_text = "Send Message"

    def get_success_url(self):
        self.success_url = reverse_lazy('ledgeritem-list', kwargs={'pk':self.kwargs.get('pk')})

    def get_context_data(self, **kwargs):
        context = super(LedgerItemInquireView, self).get_context_data(**kwargs)
        context['heading_text'] = self.heading_text
        context['button_text'] = self.button_text

        ledger_item = get_object_or_404(LedgerItem, pk=self.kwargs.get('pk'))

        # sending the inquiry to
        recipiant = ledger_item.created_by.email

        # the sender is the logged in user
        sender = self.request.user.email

        # forming the subject
        subject = "%s: %s" % (ledger_item.ledger, ledger_item)

        initial_dict = {
            'to_user':recipiant,
            'from_user':sender,
            'subject':subject,
            'message':""
        }
        
        # instantiate the form with initial data
        context['form'] = app.forms.InquireForm(initial=initial_dict)
        
        # return the context
        return context
    
    def form_invalid(self, form):
        return super(LedgerItemInquireView, self).form_invalid(form)

    def form_valid(self, form):

        print("about to print the data")

        # send the email to the user
        print(form.cleaned_data)

        return super(LedgerItemInquireView, self).form_valid(form)