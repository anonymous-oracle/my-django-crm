from django.shortcuts import render, redirect, reverse
from django.core.mail import send_mail
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from .models import Lead, Agent
from . import forms
from . import utils

# Create your views here.

class SignupView(generic.CreateView):
    template_name = 'registration/signup.html'
    form_class = forms.CustomUserCreationForm

    def get_success_url(self) -> str:
        return reverse('login')

class LandingPageView(generic.TemplateView):
    template_name = 'landing.html'

class LeadListView(LoginRequiredMixin, generic.ListView):
    template_name = 'leads/lead_list.html'
    queryset = Lead.objects.all() # the queryset of the model that has to be listed
    context_object_name = "leads" # this will rename the default context variable which is called as objects_list to leads

    def get(self, request, *args, **kwargs):
        return super().get(self, request, *args, **kwargs) # simply demonstrates the ListView class's get method to handle requests


class LeadDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = 'leads/lead_detail.html'
    queryset = Lead.objects.all() # the view needs a query set to filter the particular lead for the detail lead view
    context_object_name = "lead"

class LeadCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = 'leads/lead_create.html'
    form_class = forms.LeadModelForm

    def post(self, request, *args, **kwargs):
        return super().post(self, request, *args, **kwargs)

    def get_success_url(self) -> str:
        return reverse('leads:home')

    # this method was selected based on the method in super class of the CreateView
    def form_valid(self, form): # if form is valid an email will be sent
        send_mail(subject="Lead created", message="Visit the website to view the changes",
                  from_email='test@test.com', recipient_list=['test2@test.com'])
        # this is how the form validation works
        return super(LeadCreateView, self).form_valid(form)

class LeadUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = 'leads/lead_update.html'
    queryset = Lead.objects.all() # the view needs a query set to filter the particular lead for the detail update view
    form_class = forms.LeadModelForm

    def get_success_url(self) -> str:
        return reverse('leads:home')

class LeadDeleteView(LoginRequiredMixin, generic.DeleteView):
    template_name = 'leads/lead_delete.html'
    queryset = Lead.objects.all()

    def get_success_url(self) -> str:
        return reverse('leads:home')

def landing_page(request: HttpRequest):
    return render(request=request, template_name='landing.html')

def lead_list(request: HttpRequest):

    # context = {
    #     "name" : request.GET.get('name','anonymous')
    # }

    # return HttpResponse("Hello from home page")
    leads = Lead.objects.all()
    context = {"leads": leads}
    return render(
        request=request, template_name="leads/lead_list.html", context=context
    )


def second_home_page(request: HttpRequest):
    return render(request=request, template_name="second_page.html")


def lead_detail(request: HttpRequest, pk):
    lead = Lead.objects.get(id=pk)
    context = {"lead": lead}
    return render(
        request=request, template_name="leads/lead_detail.html", context=context
    )


# def lead_create(request: HttpRequest):
#     if request.method.lower() == 'post':
# form = forms.LeadForm(request.POST)
# if form.is_valid():
#     if not form.cleaned_data.get('agent'):
#         form.cleaned_data.update(agent = Agent.objects.first())
#     lead = Lead.objects.create(**form.cleaned_data)
#     lead.save()
#     return redirect('/leads')
#             # return HttpResponse(f"Created a lead for {form.cleaned_data.get('first_name')}")
#     elif request.method.lower() == 'get':
#         context = {
#             "form": forms.LeadForm()
#         }
#         return render(request=request, template_name='leads/lead_create.html', context = context)
#     else:
#         response = HttpResponse()
#         response.status_code = 404
#         response.content = "<h1>Not found</h1>"
#         return response


def lead_create(request: HttpRequest):
    if request.method.lower() == "post":
        post_data = request.POST.dict()
        form = forms.LeadModelForm(post_data)
        if form.is_valid():
            if not form.cleaned_data.get("agent"):
                agent = utils.assign_agent_for_lead()
                post_data.update(agent=agent)
                form = forms.LeadModelForm(post_data)
            form.save()  # for a model form, calling the .save() method after validation is sufficient to save the lead details
            return redirect("/leads")
            # return HttpResponse(f"Created a lead for {form.cleaned_data.get('first_name')}")
    elif request.method.lower() == "get":
        context = {"form": forms.LeadModelForm()}
        return render(
            request=request, template_name="leads/lead_create.html", context=context
        )
    else:
        response = HttpResponse()
        response.status_code = 404
        response.content = "<h1>Not found</h1>"
        return response


# def lead_update(request: HttpRequest, pk):
#     if request.method.lower() == 'get':
#         lead = Lead.objects.get(id=pk)
#         context = {
#             'lead': lead,
#             'form': forms.LeadForm()
#         }
#         return render(request=request, template_name='leads/lead_update.html', context=context)
#     elif request.method.lower() == 'post':
#         form = forms.LeadForm(request.POST)
#         if form.is_valid():
#             if not form.cleaned_data.get('agent'):
#                 form.cleaned_data.update(agent = Agent.objects.first())
#             Lead.objects.filter(id=pk).update(**form.cleaned_data)
#         return redirect('/leads')
#     else:
#         response = HttpResponse()
#         response.status_code = 404
#         response.content = "<h1>Not found</h1>"
#         return response


def lead_update(request: HttpRequest, pk):

    lead = Lead.objects.get(id=pk)
    if request.method.lower() == "get":
        context = {"lead": lead, "form": forms.LeadModelForm(instance=lead)}
        return render(
            request=request, template_name="leads/lead_update.html", context=context
        )
    elif request.method.lower() == "post":
        form = forms.LeadModelForm(request.POST, instance=lead)
        if form.is_valid():
            if not form.cleaned_data.get("agent"):
                lead.agent = utils.assign_agent_for_lead()
            form.save()
        return redirect("/leads")
    else:
        response = HttpResponse()
        response.status_code = 404
        response.content = "<h1>Not found</h1>"
        return response


def lead_delete(request: HttpRequest, pk):
    Lead.objects.get(id=pk).delete()
    return redirect("/leads")
