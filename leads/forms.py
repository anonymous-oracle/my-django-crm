from typing import Any, Mapping
from django import forms
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.contrib.auth import get_user_model
from django.forms.renderers import BaseRenderer
from django.forms.utils import ErrorList
from .models import Lead, Agent

User = get_user_model() # fetches the current project's User model instead of the default user model 

class LeadForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    age = forms.IntegerField(min_value=0)


class LeadModelForm(forms.ModelForm):

    agent = forms.ModelChoiceField(
        Agent.objects, required=False
    )  # adding a model choice field

    class Meta:
        model = Lead
        fields = ("first_name", "last_name", "age", "agent")

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username',)
        field_classes = {'username': UsernameField}

class AssignAgentForm(forms.Form):
    agent = forms.ModelChoiceField(queryset=Agent.objects.none()) # default value if appropriate data is not available

    def __init__(self, *args, **kwargs) -> None:

        request = kwargs.pop('request') # popping this out because this is not a valid keyword arguement
        # pk = kwargs.pop('pk') # popping for the same reason as above; needed if the self.kwargs is being updated to the get_form_kwargs as this will have the primary key parameter 'pk'

        agents = Agent.objects.filter(organisation=request.user.userprofile) # provides a list of agents belonging to the same organisation of the organiser
        
        super(AssignAgentForm, self).__init__(*args, **kwargs)
        self.fields['agent'].queryset = agents

class LeadCategoryUpdateForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ("category",)