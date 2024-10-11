from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from .models import Lead

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