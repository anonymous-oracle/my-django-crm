from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

# Create your views here.
def home_page(request: HttpRequest):
    # return HttpResponse("Hello from home page")
    return render(request=request, template_name='leads/home_page.html')

def second_home_page(request: HttpRequest):
    return render(request=request, template_name='second_page.html')