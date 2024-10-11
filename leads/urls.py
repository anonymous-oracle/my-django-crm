from django.urls import path
from .views import lead_list, second_home_page

app_name = 'leads'

urlpatterns = [
    path('', lead_list, name='leads-home'),
    path('second/', second_home_page, name='leads-second-home'),
]