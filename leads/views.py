from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.views.generic import ListView, TemplateView, DetailView, CreateView, UpdateView
from .models import Lead, Agent
from . import forms
from . import utils

# Create your views here.

class LandingPageView(TemplateView):
    template_name = 'landing.html'

class LeadListView(ListView):
    template_name = 'leads/lead_list.html'
    queryset = Lead.objects.all() # the queryset of the model that has to be listed
    context_object_name = "leads" # this will rename the default context variable which is called as objects_list to leads

class LeadDetailView(DetailView):
    template_name = 'leads/lead_detail.html'
    queryset = Lead.objects.all()
    context_object_name = "lead"

class LeadCreateView(CreateView):
    template_name = 'leads/lead_create.html'
    form_class = forms.LeadModelForm

    def get_success_url(self) -> str:
        return redirect('leads:home')

class LeadUpdateView(UpdateView):
    template_name = 'leads/lead_update.html'
    form_class = forms.LeadModelForm

    def get_success_url(self) -> str:
        return redirect('leads:home')


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
