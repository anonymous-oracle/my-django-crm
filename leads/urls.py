from django.urls import path
from . import views

app_name = "leads"

urlpatterns = [
    # path("", views.lead_list, name="home"),
    path("", views.LeadListView.as_view(), name="home"),
    path("second/", views.second_home_page, name="second-home"),
    # path("<int:pk>/", views.lead_detail, name="detail"),
    path("<int:pk>/", views.LeadDetailView.as_view(), name="detail"),
    # path("create/", views.lead_create, name="create"),
    path("create/", views.LeadCreateView.as_view(), name="create"),
    # path("<int:pk>/update", views.lead_update, name="update"),
    path("<int:pk>/update", views.LeadUpdateView.as_view(), name="update"),
    path("<int:pk>/delete", views.lead_delete, name="delete"),
]
