from typing import Any
from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render, reverse
from  django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from leads.models import Agent
from .forms import AgentModelForm

class AgentListView(LoginRequiredMixin, generic.ListView):
    template_name = "agents/agent_list.html"
    
    def get_queryset(self) -> QuerySet[Any]:
        return Agent.objects.all()
    
class AgentCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = "agents/agent_create.html"
    form_class = AgentModelForm

    def get_success_url(self) -> str:
        return reverse('agents:agent-list')
    
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        agent = form.save(commit=False) # not to commit to the database immediately but to save it in a variable for now
        agent.organisation = self.request.user.userprofile # access to the user object because of the LoginRequiredMixin
        agent.save() # saving it now
        
        # since the AgentCreateView form class inherits from the CreateView class, which in turn inherits from the form template mixin class and the BaseCreateView itself, the AgentCreateView class is being passed as the template Mixin class for the super() call and the self class reference of the AgentCreateView class is being passed as the CreateView/BaseCreateview class on which .form_valid function is being called
        return super(AgentCreateView, self).form_valid(form)