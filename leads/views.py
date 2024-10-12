from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from .models import Lead, Agent
from . import forms

# Create your views here.
def lead_list(request: HttpRequest):

    # context = {
    #     "name" : request.GET.get('name','anonymous')
    # }

    # return HttpResponse("Hello from home page")
    leads = Lead.objects.all()
    context = {
        'name': request.GET.get('name', 'anonymous'),
        'leads' : leads
    }
    return render(request=request, template_name='leads/lead_list.html', context=context)

def second_home_page(request: HttpRequest):
    return render(request=request, template_name='second_page.html')

def lead_detail(request: HttpRequest, pk):
    lead = Lead.objects.get(id=pk)
    context = {
        "lead": lead
    }
    return render(request=request, template_name='leads/lead_detail.html', context=context)

# def lead_create(request: HttpRequest):
#     if request.method.lower() == 'post':
#         form = forms.LeadForm(request.POST)
#         if form.is_valid():
#             if not form.cleaned_data.get('agent'):
#                 form.cleaned_data.update(agent = Agent.objects.first())
#             lead = Lead.objects.create(**form.cleaned_data)
#             lead.save()
#             return redirect('/leads')
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
    if request.method.lower() == 'post':
        form = forms.LeadModelForm(request.POST)
        if form.is_valid():
            if not form.cleaned_data.get('agent'):
                form.cleaned_data.update(agent = Agent.objects.first())
            form.save() # for a model form, calling the .save() method after validation is sufficient to save the lead details
            return redirect('/leads')
            # return HttpResponse(f"Created a lead for {form.cleaned_data.get('first_name')}")
    elif request.method.lower() == 'get':   
        context = {
            "form": forms.LeadModelForm()
        }
        return render(request=request, template_name='leads/lead_create.html', context = context)
    else:
        response = HttpResponse()
        response.status_code = 404
        response.content = "<h1>Not found</h1>"
        return response