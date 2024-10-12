from django.urls import path
from . import views

app_name = 'leads'

urlpatterns = [
    path('', views.lead_list, name='leads-home'),
    path('second/', views.second_home_page, name='leads-second-home'),
    path('<int:pk>/', views.lead_detail, name='leads-detail'),
    path('create/', views.lead_create, name='leads-create'),
    path('<int:pk>/update', views.lead_update, name='leads-update'),
    path('<int:pk>/delete', views.lead_delete, name='leads-delete')
]